CREATE TABLE users (
    user_id INTEGER PRIMARY KEY,
    created_at TIMESTAMP,
    metadata JSON
);

CREATE TABLE sessions (
    session_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    start_ts TIMESTAMP,
    end_ts TIMESTAMP,
    fps REAL,
    device_info TEXT,
    FOREIGN KEY(user_id) REFERENCES users(user_id)
);

CREATE TABLE frame_samples (
    session_id INTEGER,
    ts TIMESTAMP,
    ear_left REAL,
    ear_right REAL,
    iris_h REAL,
    iris_v REAL,
    face_conf REAL,
    flags TEXT,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

CREATE TABLE blink_events (
    session_id INTEGER,
    start_ts TIMESTAMP,
    end_ts TIMESTAMP,
    duration_ms REAL,
    min_ear REAL,
    is_incomplete BOOLEAN,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);

CREATE TABLE window_metrics (
    session_id INTEGER,
    window_start TIMESTAMP,
    window_end TIMESTAMP,
    blink_rate REAL,
    ibi_mean REAL,
    incomplete_ratio REAL,
    gaze_variance REAL,
    fixation_ratio REAL,
    off_center_ratio REAL,
    risk_score REAL,
    FOREIGN KEY(session_id) REFERENCES sessions(session_id)
);
