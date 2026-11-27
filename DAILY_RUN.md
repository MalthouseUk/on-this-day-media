# On This Day – daily run instructions

These instructions are for the nightly scheduled task that prepares the next day's five posts
for the "On This Day" Facebook Page (owner: Simon, UK, Europe/London time).

## The five posts (always in this order)
1. **Born on this day**: multi-photo post (cover + one page per person, 4:5 portrait 1080x1350). 6 people.
2. **We remember** (died on this day): multi-photo post. 4 people.
3. **Events in history**: video, 3–4 events.
4. **Top of the charts**: video, UK and US Number 1 for 3 different years.
5. **Sport on this day**: video, 3–4 moments.

## Content rules
- Audience is mostly older readers in the UK. UK English spelling, warm and slightly witty "quality newspaper" tone.
- Mix of eras and fields. Include British people/events where possible, plus international names.
- Choose well-known, family-friendly subjects. Avoid violent deaths, suicides, disasters and
  atrocities as headline items. Keep any political figure strictly neutral and factual.
- Never include photos of real people, logos, copyrighted song lyrics or music.
- Do not repeat the chart years used on the previous few days if avoidable. Rotate decades.
- **Every fact must be checked with a web search before use**: birth and death dates, chart
  number ones (use officialcharts.com for UK and Wikipedia "List of Billboard Hot 100 number ones
  of YEAR" for US, matching the chart week that contains the date), and sport/history dates.
- For living people, check their **current** role/club/status (things change: e.g. a manager
  moving clubs). Never describe a living person as dead or vice versa.
- Bios: exactly 3 short paragraphs (about 20–30 words each). The first paragraph must start with
  a letter (not a quote mark) because it gets a drop cap.
- `short` is a one-line description (max ~50 characters) for the cover page.
- `born`/`died` dates in the form "26 November 1922"; use "c. 1797" if only approximate;
  `died` is null for living people.

## Build
```
pip install --break-system-packages pillow numpy   # only if missing; ffmpeg must be present
python3 tools/build_day.py YYYY-MM-DD
```
This reads `data/YYYY-MM-DD.json` (copy the shape of `data/2026-11-26.json`) and writes the
folder `YYYY-MM-DD/`. After building, look at the cover images and at least two person pages
(and check the build printed no "OVERFLOW" lines; if it did, shorten that bio and rebuild).

Commit `data/YYYY-MM-DD.json` and `YYYY-MM-DD/` to `main` and push.
Public media URL pattern:
`https://raw.githubusercontent.com/MalthouseUk/on-this-day-media/main/YYYY-MM-DD/<file>`

## Scheduling in Buffer
- Organization: "My organization" (id 6b07edec87c54196b3239129)
- Facebook Page channel "On This Day" (id 6b07ef248541f09ecbaca020)
- Read the channel's posting schedule with get_channel and use that day's five time slots, in
  order, for the five posts (born, remembered, history, charts, sport). Use mode
  `customScheduled` with `dueAt` in Europe/London time, `schedulingType` automatic,
  `metadata.facebook.type` = "post". Skip any slot already in the past.
- Images: one asset per picture, in file-name order, each with short alt text.
- Videos: a single video asset.
- Caption text: the matching section of `captions.txt`.
- Before creating posts, list the posts already scheduled for that date and do not duplicate.
- Buffer's free plan holds max 10 scheduled posts at once.

## Finish
Send Simon one short summary: the date, the names/events/chart songs in each post, the times
scheduled, and anything uncertain. Remind him he can edit or delete any post in Buffer before
it goes out.
