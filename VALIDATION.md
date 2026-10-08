# Validation

232 automated tests passed: 172 mathematics/progression/app checks, 56 diagram checks and 4 music checks. Diagram tests render every visual template across all three levels, verify PNG output and serialisable finite data, check both ambiguous triangle configurations against the given sides and angle, validate annular-sector and feasible-region geometry, and exercise images in the question and completed review.

Existing checks include original question generation, independent upper-level examples, numeric input safety, bilingual sessions, staged hints and scoring, retries, consent-based persistence and teacher login.

`python verify_project.py` passed required-source parsing and mixed-session generation for both curricula at every level and in progression mode.

Generated diagram samples were visually inspected and the ambiguous-triangle layout was improved. Streamlit AppTest exercised the application flows. Full browser screenshot verification was unavailable in the build environment; check layout on classroom devices before sharing.

This is original basic-to-exam-style practice across the topic menus, not exhaustive syllabus coverage or official examination method marking.

Music checks cover packaged audio and static-serving configuration, removal of the Focus toggle, sidebar component mounting, and a JavaScript audio mock exercising blocked autoplay, gesture start, continuous state across rerenders, loop/volume settings, user pause and navigation. A local HTTP check returned 200 with audio/mpeg for the packaged MP3. The MP3 codec and duration were validated with ffprobe. These are not a real-browser listening test; browser autoplay policies still apply.

Playback repair: the exact MP3 bytes are embedded directly, eliminating static URL/configuration dependencies. A browser acknowledgement avoids resending the large source on later question updates. Regression tests cover acknowledgement, source byte equality, page reconnection and the pointerdown/Play-click race. The first 10 seconds decoded successfully and contained non-silent audio. Browser playback still requires a user gesture when autoplay is blocked; no real-browser listening test was available.
