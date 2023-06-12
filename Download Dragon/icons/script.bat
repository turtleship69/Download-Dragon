for /r %%i in (icon.png) do (
    magick "%%i" -resize 16x16 "%%~dpiicon-16.png"
    magick "%%i" -resize 32x32 "%%~dpiicon-32.png"
    magick "%%i" -resize 48x48 "%%~dpiicon-48.png"
    magick "%%i" -resize 64x64 "%%~dpiicon-64.png"
    magick "%%i" -resize 96x96 "%%~dpiicon-96.png"
    magick "%%i" -resize 128x128 "%%~dpiicon-128.png"
    magick "%%i" -resize 256x256 "%%~dpiicon-256.png"
)