class FchartSettings:
    def __init__(self, limiting_magnitude_stars=13.8, limiting_magnitude_deepsky=12.5, fieldsize=7.0):
        self.limiting_magnitude_stars = limiting_magnitude_stars,
        self.limiting_magnitude_deepsky = limiting_magnitude_deepsky
        self.paperwidth = 180.0  # mm
        self.fieldsize = fieldsize   # degrees
        self.force_messier = False
        self.force_asterisms = False
        self.force_unknown = False
        self.output_dir = '/tmp'
        self.extra_positions_list = []
        self.language = "EN"
        self.sourcelist = []
        self.output_type = "PDF"
        self.caption = False
        self.fieldcentre = (-1, -1)

    def add_target(self, ra, dec, label):
        self.sourcelist.append("{0},{1},{2}".format(ra, dec, label))


def generate_fchart(settings):
    print settings
