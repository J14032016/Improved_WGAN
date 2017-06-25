import tensorflow as tf


class FCCritic:
    def __init__(self, img_size, channels):
        self.img_size = img_size
        self.channels = channels

    def __call__(self, image, reuse=None):
        with tf.variable_scope("Critic", reuse=reuse):
            image = tf.reshape(image, [-1, self.img_size * self.img_size * self.channels])

            image = tf.layers.dense(image, 512, tf.nn.relu)
            image = tf.layers.dense(image, 512, tf.nn.relu)
            image = tf.layers.dense(image, 1)
            return image


class ConvCritic:
    def __init__(self, img_size, channels):
        self.img_size = img_size
        self.channels = channels

    def __call__(self, image, reuse=None):
        with tf.variable_scope("Critic", reuse=reuse):
            act = tf.nn.relu
            kernel3 = (3, 3)
            kernel4 = (4, 4)
            pad1 = [[0, 0], [1, 1], [1, 1], [0, 0]]
            pad2 = [[0, 0], [2, 2], [2, 2], [0, 0]]

            kwargs3 = {"kernel_size": kernel3, "strides": (1, 1), "padding": "valid"}
            kwargs4 = {"kernel_size": kernel4, "strides": kernel4, "padding": "valid"}

            image = tf.pad(image, pad1, mode="SYMMETRIC")
            image = tf.layers.conv2d(image, filters=64, **kwargs3, activation=act)

            # image is 64x64x1024
            image = tf.layers.conv2d(image, filters=128, **kwargs4, activation=act)

            # image is 16x16x1024
            image = tf.pad(image, pad1, mode="SYMMETRIC")
            image = tf.layers.conv2d(image, filters=256, **kwargs3, activation=act)

            # image is 16x16x1024
            image = tf.layers.conv2d(image, filters=512, **kwargs4, activation=act)

            # image is 4x4x1024
            image = tf.pad(image, pad1, mode="SYMMETRIC")
            image = tf.layers.conv2d(image, filters=1024, **kwargs3, activation=act)

            # image is 4x4x1024
            image = tf.reshape(image, [-1, 4 * 4 * 1024])
            image = tf.layers.dense(image, 1)

            print(image.shape)
            assert image.shape[1] == 1
            return image


class DCGANCritic:
    def __init__(self, img_size, channels):
        pass

    def __call__(self, image, reuse=None):
        """
        Works only for 64x64

        :param image:
        :param reuse:
        :return:
        """
        with tf.variable_scope("Critic", reuse=reuse):
            kwargs = {"kernel_size": (5, 5), "strides": (2, 2), "padding": "same", "activation": tf.nn.relu}

            image = tf.layers.conv2d(image, filters=64, **kwargs)
            image = tf.layers.conv2d(image, filters=128, **kwargs)
            image = tf.layers.conv2d(image, filters=256, **kwargs)
            image = tf.layers.conv2d(image, filters=1024, **kwargs)
            image = tf.reshape(image, [-1, 4 * 4 * 1024])
            image = tf.layers.dense(image, 1)
            return image
