import webvtt
import pandas as pd


def convert_to_time(timestamp_str):
    h, m, s, ms = map(int, timestamp_str.replace('.', ':').split(':'))

    return h, m, s, ms


def get_total_ms(timestamp_str) -> float:
    h, m, s, ms = convert_to_time(timestamp_str)
    total_milliseconds = h * 3600000 + m * 60000 + s * 1000 + ms
    # Convert the result to a float
    total_milliseconds_float = float(total_milliseconds) / 1000.0
    return total_milliseconds_float


def compare_start_time(f_start: str, s_start: str, threshold: float = 1.459) -> bool:
    f_start_total = get_total_ms(f_start)
    s_start_total = get_total_ms(s_start)
    # print(f_start_total, s_start_total)
    return (s_start_total - f_start_total) < threshold


def delete_two_milliseconds(timestamp_str):
    # Split the timestamp string into hours, minutes, seconds, and milliseconds
    h, m, s, ms = convert_to_time(timestamp_str)

    # Convert back to the WebVTT format string (hh:mm:ss.mmm)
    rounded_timestamp_str = "{:02d}:{:02d}:{:02d}".format(
        h, m, s)
    return rounded_timestamp_str


def round_milliseconds(caption):
    caption = delete_two_milliseconds(caption.start)

    return caption


def prepare(captions):
    new_subtitles_en = []
    i = 0
    while i < len(captions) - 1:
        temp = 1
        for j in range(i+1, len(captions)):
            if compare_start_time(captions[i].start, captions[j].start):
                captions[i].text = captions[i].text + " " + \
                    captions[j].text
                temp = temp + 1
            if j == len(captions) - 1:
                new_subtitles_en.append(captions[i])
        i = i + temp

    return new_subtitles_en


def virtualize(caption1, caption2):
    cap1_start_times = []
    cap1_texts = []

    cap2_start_times = []
    cap2_texts = []

    for cap in caption1:
        cap1_start_times.append(round_milliseconds(cap))
        cap1_texts.append(cap.text)

    caption1_df = pd.DataFrame({
        'Time': cap1_start_times,
        'Text': cap1_texts
    })

    for cap in caption2:
        cap2_start_times.append(round_milliseconds(cap))
        cap2_texts.append(cap.text)

    caption2_df = pd.DataFrame({
        'Time': cap2_start_times,
        'Text': cap2_texts
    })
    
    merged_caption_df = pd.merge(
        caption1_df, caption2_df, on='Time', suffixes=('subtitle', 'translate'), how='left')

    merged_caption_df.to_csv('results.csv')
    print(merged_caption_df)


def main():
    # Load the .vtt files
    subtitles_en = webvtt.read('en.vtt')
    subtitles_es = webvtt.read('de.vtt')

    subtitles_en = prepare(subtitles_en) if len(
        subtitles_en) > len(subtitles_es) else prepare(subtitles_es)

    virtualize(subtitles_en, subtitles_es)

    # for sub in subtitles_es:
    #     print(sub.start)


if __name__ == '__main__':
    main()
