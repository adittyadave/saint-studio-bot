{ pkgs }: {
  deps = [
    pkgs.python310
    pkgs.ffmpeg
  ];
  env = {
    PYTHONUNBUFFERED = "1";
  };
}
