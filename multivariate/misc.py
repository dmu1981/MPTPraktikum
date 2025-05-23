import numpy as np
import cv2

IMAGE_SHAPE = (1280, 1280, 3)
X_RANGE = (-6.0, 6.0)
Y_RANGE = (-6.0, 6.0)
SAMPLES_PER_CLUSTER = 512


def xy_to_image(x, y):
    x = int((x - X_RANGE[0]) / (X_RANGE[1] - X_RANGE[0]) * IMAGE_SHAPE[1])
    y = int((y - Y_RANGE[1]) / (Y_RANGE[0] - Y_RANGE[1]) * IMAGE_SHAPE[0])
    return x, y


def draw_cluster(image, cluster, col=(0.0, 0.07, 0.46)):
    for pt in cluster:
        x, y = xy_to_image(pt[0], pt[1])

        cv2.circle(image, (x, y), 1, col, -1)


def draw_mahalanobis(image, mu, cov, col=(0.0, 0.14, 0.92)):
    try:
        cholesky = np.linalg.cholesky(cov)
    except np.linalg.LinAlgError:
        return

    for scale in [1.0, 2.0, 3.0]:
        x0, y0 = None, None
        for rad in np.linspace(0.0, 2.0 * np.pi, 180):
            s, c = np.sin(rad), np.cos(rad)
            pt = scale * cholesky @ np.array([[s, c]]).T
            x1, y1 = xy_to_image(pt[0] + mu[0], pt[1] + mu[1])
            if x0 is not None:
                cv2.line(image, (x0, y0), (x1, y1), col, 2)
            x0, y0 = x1, y1


def draw_text(image, mu, cov, yOffset=0, col=(0.0, 0.14, 0.92)):
    cv2.putText(
        image,
        f"mu = ({mu[0]:.1f}, {mu[1]:.1f})",
        (30, 30 + yOffset),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        col,
    )

    cv2.putText(
        image, f"cov = ", (28, 75 + yOffset), cv2.FONT_HERSHEY_SIMPLEX, 0.6, col
    )
    cv2.putText(
        image,
        f"{cov[0][0]:.1f}, {cov[0][1]:.1f}",
        (105, 60 + yOffset),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        col,
    )
    cv2.putText(
        image,
        f"{cov[1][0]:.1f}, {cov[1][1]:.1f}",
        (105, 90 + yOffset),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        col,
    )


def draw_axes(image):
    col = (0.1, 0.1, 0.1)
    x0, y0 = xy_to_image(X_RANGE[0], 0.0)
    x1, y1 = xy_to_image(X_RANGE[1], 0.0)
    cv2.line(image, (x0, y0), (x1, y1), col, 2)

    x0, y0 = xy_to_image(0.0, Y_RANGE[0])
    x1, y1 = xy_to_image(0.0, Y_RANGE[1])
    cv2.line(image, (x0, y0), (x1, y1), col, 2)

    for x in [-5.0, -4.0, -3.0, -2.0, -1.0, 1.0, 2.0, 3.0, 4.0, 5.0]:
        x0, y0 = xy_to_image(x, 0.0)
        cv2.line(image, (x0, y0 - 8), (x0, y0 + 8), col, 2)
        s = f"{x:.1f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.34
        thick = 2
        textSize = cv2.getTextSize(s, font, scale, thick)
        cv2.putText(
            image, s, (x0 - textSize[0][0] // 2, y0 + 24), font, scale, col, thick
        )

    for y in [-5.0, -4.0, -3.0, -2.0, -1.0, 1.0, 2.0, 3.0, 4.0, 5.0]:
        x0, y0 = xy_to_image(0.0, y)
        cv2.line(image, (x0 - 8, y0), (x0 + 8, y0), col, 2)
        s = f"{y:.1f}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.34
        thick = 2
        textSize = cv2.getTextSize(s, font, scale, thick)
        cv2.putText(
            image, s, (x0 + 16, y0 + textSize[0][1] // 2 - 1), font, scale, col, thick
        )
