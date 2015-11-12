for /r %%F in (samples\*) do (
    count_frequency samples\%%~nxF testoracle\freqs_%%~nxF
    count_frequency samples\%%~nxF testoracle\freqs5_%%~nxF 5
)

