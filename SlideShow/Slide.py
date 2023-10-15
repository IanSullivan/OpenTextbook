import cv2
import numpy as np
import textwrap


def make_slide(idx, bullet_points):
    slide = np.full((1080, 1920, 3), 255, np.uint8)

    font = cv2.FONT_HERSHEY_COMPLEX

    text_size = cv2.getTextSize(bullet_points[0], font, 1, 2)[0]
    for i, bullet_point in enumerate(bullet_points):
        wrapped_text = textwrap.wrap(bullet_point, width=100)
        for j, line in enumerate(wrapped_text):
            y = (50 + j * int(text_size[1] * 2)) + (100 + i * int(text_size[1] * 5))
            cv2.putText(slide, line, (50, y), font, 1, (0, 0, 0), 2)

    cv2.imwrite("pics/{}.jpg".format(idx), slide)
    return "pics/{}.jpg".format(idx)


if __name__ == "__main__":
    a = ['He distinguished himself and became one of the main commanders during the popular uprising against the Italians in Montenegro in July 1941, but later collaborated with the Italians',
 'In actions against the Communist-led Yugoslav Partisans, his troops carried out several massacres against the Muslim population of Bosnia, Herzegovina and the Sandžak',
 'Participated in the anti-Partisan Case White offensive alongside Italian forces',
 'Đurišić was captured by the Germans in May 1943, escaped and was recaptured.',
 'His heroic nature earned him the highest accolades.']
    make_slide("0", a)
