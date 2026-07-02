# SRT to TSV

Converts SRT subtitle files to TSV format with columns `Index`, `Start`, `End`, and `Text`.

The resulting TSV can be further enriched with additional columns derived from the subtitle context — for example, generating text-to-image prompts from the spoken content.

## Usage

Place `.srt` files in `USER-FILES/04.INPUT/` and run:

```
python run.py
```

Output TSV files are written to `USER-FILES/05.OUTPUT/{timestamp}_TSV/`.
