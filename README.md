# EXCELerate · AddMath Arena

A separate Streamlit practice app for learners aged 16–18. It includes Cambridge IGCSE Additional Mathematics 0606 and Malaysia SPM KSSM Additional Mathematics topic paths. English, Bahasa Melayu and side-by-side bilingual modes apply to questions, hints and worked solutions.

## Start locally

Use Python 3.11 or 3.12. From this folder:

```sh
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Deploy as a NEW app — step by step

Keep your Penguin MathQuest repository. This project uses a separate repository.

1. Download and extract `EXCELerate_AddMath_Arena.zip`.
2. In GitHub, create a new repository named `excelerate-addmath-arena`.
3. Click **Add file → Upload files**. Upload the contents INSIDE the extracted `addmath_arena` folder. Do not upload the ZIP itself.
4. At the repository's top level, confirm these files exist: `app.py`, `bank.py`, `progression.py`, `checker.py`, `curriculum.py`, `storage.py`, and `requirements.txt`. Include `README.md`, `verify_project.py`, `requirements-dev.txt` and the `tests` folder too.
5. Upload `.streamlit/config.toml` as well. Windows may hide this folder; GitHub → Add file → Create new file also lets you create a file with that exact path and paste the supplied contents. The in-app styles still work if this theme file is missed.
6. Commit directly to `main`.
7. At https://share.streamlit.io choose **Create app**. Select the NEW repository, `main`, and `app.py` as the main file. Deploy.
8. For teacher access, open the app's Settings → Secrets and add the top-level line below, substituting a private password:

```toml
teacher_password = "REPLACE_WITH_YOUR_PRIVATE_PASSWORD"
```

9. Save secrets. If necessary, use the app menu → Reboot. Open **Teacher dashboard** from the sidebar and log in.
10. Run a five-question test in each course before sharing the app with students.

No previous Penguin app modules, image assets, paid API keys or AI subscriptions are needed. All artwork is created in CSS, and all questions are generated locally from original templates.

## Panduan ringkas Bahasa Melayu

Ekstrak ZIP dan muat naik semua fail dalam folder `addmath_arena` ke repositori GitHub baharu. Pastikan `app.py` dan `requirements.txt` berada pada aras utama. Dalam Streamlit Community Cloud, pilih repositori baharu, cabang `main` dan fail utama `app.py`. Tetapkan `teacher_password` dalam Settings → Secrets untuk akses guru. Jangan letakkan kata laluan dalam GitHub.

## What works

- Distinct Cambridge and SPM menus; SPM Form 4/Form 5 filtering.
- 14 Cambridge menu topics and 18 SPM menu topics, with 24 generator categories across both paths.
- Original basic templates plus distinct linked-step and exam-style templates for every topic; 5/10/15-question topic or mixed sessions.
- Numeric and multi-answer questions. Multiple roots are checked without requiring a particular order; coordinates/components are ordered and labelled.
- Worked solution steps in both languages, properly typeset fractions, roots, logarithms and integrals.
- Arithmetic input such as `1/2`, `sqrt(3)` and `2*pi/3`. Input is parsed using a restricted, bounded AST; it is not executed as Python code.
- Practice XP, streaks, staged bilingual hints, per-level results, end-of-session review, recommended topics and a queue to retry missed questions.
- Interactive quadratic, sine, exponential and logarithmic graph exploration with labelled axes and reference curves.
- Dark lime/violet study-game styling, CSS chrome orb, sticker accents and a calmer Focus mode. No flashing animation or external web fonts.
- Private teacher login, opt-in completed-session storage and CSV export. No public nickname leaderboard.

## Scope and assessment limits

The app now offers **a basic-to-exam-style progression for every topic**. Warm-up targets core applications; Level up links multiple operations and interpretations; Boss mode uses multi-part reasoning, restrictions and contexts. Build my skills automatically moves through all three stages within a session, while individual levels remain selectable. Progression is scheduled, not an adaptive mastery gate: incorrect answers do not prevent the next stage. See `PROGRESSION_GUIDE.md` for the topic-by-topic ladder. These are original practice templates, not a complete examination preparation course or official difficulty ratings. A multi-part question earns XP only when all numerical parts are correct on the first valid submission. The first hint costs 3 XP if correct; further staged hints have no additional penalty. Worked solutions become available after submission. There is no automated marking of written proofs, algebraic expressions in x, full graphical constructions or examination method marks. Differentiation prompts ask for numerical gradients or stationary-point coordinates; integration prompts use definite values or initial conditions.

The Cambridge menu references the 2025–2027 0606 syllabus, not the 2028–2030 syllabus. The SPM menu references the KSSM Form 4/Form 5 DSKP. All problems are original templates, not reproduced official examination questions. Independent classroom review of terminology and teaching suitability is encouraged before assessment use.

The student works on paper and enters final numerical answers. Single-answer fields accept a real number or arithmetic expression. Multiple fields are supplied for roots, coordinates and vector components. Trigonometric input functions use radians. Rounded answers are accepted only when the prompt requests rounding, using an explicit absolute tolerance.

## Data and teacher access

A student must check the private saving option before a completed session is written to the teacher database. Without consent, results remain in that browser session and are downloadable by the student. Reloading may reset session progress. A nickname is not a verified identity.

SQLite records are stored in `data/arena.sqlite3` by default. Streamlit Community Cloud local files are **not durable storage**: records may be lost after reboot/redeployment or infrastructure changes. Export records regularly. For reliable long-term records, deploy on a host with a persistent volume and set `ADDMATH_DB` to the database path on that volume, or add a managed database integration. Do not commit student databases or secrets to GitHub.

Records contain nickname, course, form, topic, level, score, counts, best streak, UTC completion time and submitted answers. The password is read from Streamlit Secrets; the login token is scoped to the current session. Changing the configured password invalidates the previous token on the next rerun.

## Verification

```sh
python verify_project.py
python -m pip install -r requirements-dev.txt
python -m pytest tests -q
```

The tests cover generator availability and diversity, independently calculated mathematics examples, valid and invalid answer inputs, database duplication prevention, spreadsheet-formula escaping, full student sessions, bilingual SPM selection, private saving, retry flows, graph lab and the teacher password gate.

Browser rendering and mobile polish should also be checked after deployment. Streamlit's AppTest verifies widget flows, not pixel-perfect screenshots.

## Sources and design references

- Cambridge International, 0606 syllabus for examinations in 2025–2027: https://www.cambridgeinternational.org/Images/662470-2025-2027-syllabus.pdf
- Ministry of Education DSKP reference collection: https://sites.google.com/moe-dl.edu.my/td2addmath/dskp
- Ministry-authored 2018 KSSM Mathematics Additional Form 4/Form 5 document, hosted copy: https://fliphtml5.com/nrrws/mmlv/DSKP_KSSM_MATEMATIK_TAMBAHAN_T4_DAN_T5/
- Canva 2026 design forecast, especially retro-tech experimentation, expressive layouts and material-inspired surfaces: https://www.canva.com/newsroom/news/design-trends-2026/
- Streamlit deployment and secrets: https://docs.streamlit.io/deploy/streamlit-community-cloud

This app is independently created by EXCELerate Learning Space. It is not endorsed by Cambridge International, KPM or Canva.
