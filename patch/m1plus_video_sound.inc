/* M1 Plus: the sound from an ffmpeg of its own. patch/video.c includes this where it stood (docs/m1plus-roadmap.md U1c). */
#if M1PLUS
        /* The sound from an ffmpeg of its own. One ffmpeg writing both stops on the picture's pipe
         * until it reaches the file's first sound, which an mp4 interleaved by the second puts 25
         * frames (15 MB here) on, while the picture waits for the sound's clock: the first frame
         * stays. Without a sound stream this one ends at once, and the picture goes by the wall. */
        ffmpeg_argv(args, ss, at, argv[2], 0);
        int apid = -1;
        if (audio) {
            const char *aa[] = { FFMPEG, "-nostdin", "-loglevel", "quiet", "-ss", ss, "-i", argv[2],
                                 "-vn", "-map", "0:a:0", "-ac", "2", "-ar", "48000", "-f", "s16le",
                                 "pipe:4", 0 };
            if (!(apid = fork())) {
                move_fd(ap[1], 4);
                execv(FFMPEG, aa);
                _exit(127);
            }
        }
#endif
