from PIL import Image, ImageFont, ImageDraw
from django.conf import settings


class SigImage():

    def __init__(self, user, challenges, inverted=False):
        self.text_color = (0, 0, 0)
        self.bg_color = (255, 255, 255)
        if inverted:
            self.text_color, self.bg_color = self.bg_color, self.text_color
        self.user = user
        self.challenges = challenges
        self.im = Image.new('RGB', (300, len(challenges) * 10 + 10), self.bg_color)
        self.dr = ImageDraw.Draw(self.im)
        self.font = ImageFont.truetype(settings.STATIC_ROOT + "/fonts/LiberationMono-Regular.ttf", 10)

    def draw_row(self, text, observed, total, rownum):
        self.dr.text((1, rownum * 10), "{0}:".format(
            text), self.text_color, self.font
        )
        self.dr.text((55, rownum * 10), "{0}/{1}".format(
            int(observed), int(total)
            ), self.text_color, self.font
        )
        self.dr.rectangle(
            ((100, rownum * 10 + 1), (100 + (observed / total) * 175, (rownum * 10) + 10)),
            fill=self.text_color, outline="grey"
        )

    def draw(self):
        i = 0
        for challenge in self.challenges:
            total = float(challenge.object_count)
            observed = float(challenge.objects_observed(self.user))
            self.draw_row(challenge.short_name, observed, total, i)
            i = i + 1
        self.dr.text((1, i * 10), "Total Observations: {0}".format(
            self.user.userprofile.observation_set.count()
            ), self.text_color, self.font)
        self.dr.text((185, i * 10), "Astrochallenge.com", self.text_color, self.font)
        return self.im
