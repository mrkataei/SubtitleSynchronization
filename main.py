import webvtt


def delete_two_milliseconds(timestamp_str):
    # Split the timestamp string into hours, minutes, seconds, and milliseconds
    h, m, s, ms = map(int, timestamp_str.replace('.', ':').split(':'))

    # Delete two digits from milliseconds
    rounded_ms = ms // 100
    # Convert back to the WebVTT format string (hh:mm:ss.mmm)
    rounded_timestamp_str = "{:02d}:{:02d}:{:02d}.{:03d}".format(
        h, m, s, rounded_ms)
    return rounded_timestamp_str


def round_milliseconds(captions):
    for cap in captions:
        cap.start = delete_two_milliseconds(cap.start)

    return captions


def prepare(captions):
    new_subtitles_en = []
    i = 0
    while i < len(captions) - 1:
        temp = 1
        for j in range(i+1, len(captions)):
            if captions[i].start == captions[j].start:
                captions[i].text = captions[i].text + " " + \
                    captions[j].text
                temp = temp + 1
            if j == len(captions) - 1:
                new_subtitles_en.append(captions[i])
        i = i + temp

    return new_subtitles_en


def main():
    # Load the .vtt files
    subtitles_en = webvtt.read('en.vtt')
    subtitles_es = webvtt.read('de.vtt')

    subtitles_en = prepare(subtitles_en) if len(
        subtitles_en) > len(subtitles_es) else prepare(subtitles_es)

    print(subtitles_en)


if __name__ == '__main__':
    main()
