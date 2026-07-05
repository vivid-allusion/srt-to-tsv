"""
SRT to TSV Converter

Converts SRT subtitle files to TSV format with columns: Index, Start, End, Text.
Reads from USER-FILES/04.INPUT/ and writes to USER-FILES/05.OUTPUT/{timestamp}_TSV/.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Generator

import srt
import pandas as pd
from loguru import logger


INPUT_DIR = Path("USER-FILES/04.INPUT")
OUTPUT_DIR = Path("USER-FILES/05.OUTPUT")


def find_srt_files() -> List[Path]:
    """
    Find all SRT files in the input directory.
    
    Returns:
        List of Path objects for each SRT file found.
        Exits with code 1 if no files found.
    """
    if not INPUT_DIR.exists():
        logger.error(f"Input directory does not exist: {INPUT_DIR}")
        sys.exit(1)
    
    srt_files = list(INPUT_DIR.glob("*.srt"))
    
    if not srt_files:
        logger.error(f"No SRT files found in {INPUT_DIR}")
        sys.exit(1)
    
    return sorted(srt_files)


def create_output_directory() -> Path:
    """
    Create timestamped output directory.
    
    Returns:
        Path object for the created directory.
        Exits with code 3 on directory creation failure.
    """
    timestamp = datetime.now().strftime("%y%m%d_%H%M%S")
    output_path = OUTPUT_DIR / f"{timestamp}_TSV"
    
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        logger.error(f"Failed to create output directory {output_path}: {e}")
        sys.exit(3)
    
    return output_path


def parse_srt_file(file_path: Path) -> Generator:
    """
    Parse an SRT file and return subtitle objects.
    
    Fails fast on malformed SRT with exit code 2.
    
    Args:
        file_path: Path to the SRT file to parse.
    
    Returns:
        Generator of subtitle objects.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        logger.error(f"Encoding error in {file_path.name} - UTF-8 required")
        sys.exit(2)
    except IOError as e:
        logger.error(f"Cannot read file {file_path.name}: {e}")
        sys.exit(3)
    
    try:
        subtitles = list(srt.parse(content))
    except srt.SRTParseError as e:
        logger.error(f"SRT parsing error in {file_path.name}: {e}")
        sys.exit(2)
    
    return subtitles


def format_timecode(td) -> str:
    """
    Format timedelta to SRT timecode format.
    
    Args:
        td: timedelta object
    
    Returns:
        String in format HH:MM:SS,mmm
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    milliseconds = td.microseconds // 1000
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"


def fix_timecode_gaps(subtitles: List) -> None:
    for i in range(len(subtitles) - 1):
        current = subtitles[i]
        next_sub = subtitles[i + 1]
        if next_sub.start > current.end:
            current.end = next_sub.start - timedelta(milliseconds=1)


def convert_to_dataframe(subtitles: List) -> pd.DataFrame:
    """
    Convert subtitle objects to pandas DataFrame.
    
    Args:
        subtitles: List of subtitle objects from srt.parse()
    
    Returns:
        DataFrame with columns: Index, Start, End, Text
    """
    rows = []
    
    for subtitle in subtitles:
        text = ' '.join(subtitle.content.splitlines()) if subtitle.content else ''
        
        row = {
            'Index': subtitle.index,
            'Start': format_timecode(subtitle.start),
            'End': format_timecode(subtitle.end),
            'Text': text
        }
        rows.append(row)
    
    return pd.DataFrame(rows, columns=['Index', 'Start', 'End', 'Text'])


def write_tsv(df: pd.DataFrame, output_path: Path) -> None:
    """
    Write DataFrame to TSV file with header row.
    
    Args:
        df: DataFrame to write
        output_path: Path for output TSV file
    """
    try:
        df.to_csv(output_path, sep='\t', index=False, header=True)
    except IOError as e:
        logger.error(f"Failed to write TSV file {output_path.name}: {e}")
        sys.exit(3)


def process_all_files() -> None:
    """
    Main orchestration function to process all SRT files.
    """
    srt_files = find_srt_files()
    output_dir = create_output_directory()
    
    logger.info(f"Processing {len(srt_files)} SRT file(s)")
    
    for srt_file in srt_files:
        subtitles = parse_srt_file(srt_file)
        fix_timecode_gaps(subtitles)
        df = convert_to_dataframe(subtitles)
        
        output_file = output_dir / f"{srt_file.stem}.tsv"
        write_tsv(df, output_file)
    
    logger.success(f"Converted {len(srt_files)} file(s) to {output_dir}")


if __name__ == "__main__":
    process_all_files()