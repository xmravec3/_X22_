export type Video= {
    ID: number,
    title: string,
    video_name: string,
    climber_id: number,
    climber_name: string,
    date: string,
    attempt: number,
    url: string,
    start: number,
    end: number,
    time: number,
    frames: number,
    side: string,
    skeletons: string,
    trans_matrixes: string
// VIDEO
    // ID
    // video_path / ID_RUN     {id_climber}_{date}_{ATTEMPT}.mp4 * / {id_climber}_{date}_{ATTEMPT}
    // ID_CLIMBER  **
    // DATE        **
    // ATTEMPT     **
    // URL
    // START
    // END
    // TIME_SEC
    // TIME_FRAMES
    // FINISHED
    // SIDE
    // + FRAME_RATE = TIME_SEC / TIME_FRAMES

// CLIMBER  - DONE
    // ID
    // NAME

// DATA
    // ID_RUN
    // UNROLLED_DATA - KNN SEARCH on it
    // ?MATRIXES      - 
    // ?WIRTUAL TREE  - UNROLLED_DATA * MATRIXES 
};