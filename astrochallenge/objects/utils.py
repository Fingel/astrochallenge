import fchart
import os
import string
from django.conf import settings
from numpy import *
from fchart.fonts import FontMetrics
from fchart.astrocalc import *
from fchart import deepsky_object as deepsky
from fchart.deepsky import *
from fchart.star_catalog import *
from fchart.skymap_engine import *
from fchart.pdf import *


class FchartSettings:
    def __init__(self, limiting_magnitude_stars=13.8, limiting_magnitude_deepsky=12.5, fieldsize=7.0):
        self.limiting_magnitude_stars = limiting_magnitude_stars
        self.limiting_magnitude_deepsky = limiting_magnitude_deepsky
        self.paperwidth = 180.0  # mm
        self.fieldsize = fieldsize   # degrees
        self.force_messier = False
        self.force_asterisms = False
        self.force_unknown = False
        self.output_dir = settings.MEDIA_ROOT + '/fcharts/'
        self.extra_positions_list = []
        self.language = EN
        self.sourcelist = []
        self.output_type = "PDF"
        self.caption = False
        self.fieldcentre = (-1, -1)
        self.object_id = 0
        self.content_type = 0

    def add_target(self, ra, dec, label, object_id, content_type):
        self.sourcelist.append("{0},{1},{2}".format(ra, dec, label))
        self.object_id = object_id
        self.content_type = content_type


def generate_fchart(settings):
    filename = settings.output_dir + "{0}-{1}-{2}-{3}-{4}.pdf".format(
        settings.content_type,
        settings.object_id,
        str(settings.fieldsize).replace(".", "_"),
        str(settings.limiting_magnitude_stars).replace(".", "_"),
        str(settings.limiting_magnitude_deepsky).replace(".", "_")
    )
    if os.path.isfile(filename):
        return open(filename)
    data_dir = os.path.join(fchart.get_data('catalogs'))
    font_metrics = FontMetrics(os.path.join(fchart.get_data('font-metrics')))
    starcatalog = StarCatalog(data_dir + os.sep + 'tyc2.bin', data_dir + os.sep + 'index.dat')
    deeplist = get_deepsky_list(data_dir)

    # Apply magnitude selection to deepsky list, build Messier list
    reduced_deeplist = []
    messierlist = []
    for object in deeplist:
        if object.messier > 0:
            messierlist.append(object)
            pass
        if settings.force_messier:
            if (object.mag <= settings.limiting_magnitude_deepsky and object.mag > -1) or\
                   (object.messier > 0):
                reduced_deeplist.append(object)
                pass
        else:
            if object.mag <= settings.limiting_magnitude_deepsky and \
                   object.type != deepsky.GALCL and \
                   (object.type != deepsky.STARS or settings.force_asterisms
                    or (object.messier > 0 and object.type == deepsky.STARS)) \
                   and (object.type != deepsky.PG or settings.force_unknown or
                        object.type == deepsky.PG and object.mag > -5.0):
                reduced_deeplist.append(object)
                pass
            pass
        pass
    messierlist.sort(msort)
    deepskycatalog = DeepskyCatalog(reduced_deeplist)

    for object in settings.extra_positions_list:
        rax, decx, label, labelpos = object
        print label, ':', rad2hms(rax), rad2dms(decx)
        pass

    # For all sources...
    for source in settings.sourcelist:
        # Parse sourcename
        if source.upper().rstrip().lstrip() == 'ALLMESSIER':
            print 'alles'
            for object in messierlist:
                print ''
                print 'M ' + str(object.messier)
                ra = object.ra
                dec = object.dec
                artist = PDFDrawing(filename,
                                    settings.paperwidth,
                                    settings.paperwidth,
                                    font_metrics)
                sm = SkymapEngine(artist, font_metrics, settings.language, lm_stars=settings.limiting_magnitude_stars)
                sm.set_field(ra, dec, settings.fieldsize * pi / 180.0 / 2.0)
                sm.set_caption('M ' + str(object.messier))
                sm.make_map(starcatalog, deepskycatalog,
                            settings.extra_positions_list)
                pass
        else:
            if ':' in source:
                data = source.split(',')
                if len(data) >= 3:
                    ra_str, dec_str = data[0:2]
                    ra_str = ra_str.lstrip().rstrip()
                    dec_str = dec_str.lstrip().rstrip()

                    rasplit = ra_str.split(':')
                    decsplit = dec_str.split(':')

                    rah, ram, ras = 0.0, 0.0, 0.0
                    rah = float(rasplit[0])
                    if len(rasplit) >= 2:
                        ram = float(rasplit[1])
                        pass
                    if len(rasplit) >= 3:
                        ras = float(rasplit[2])
                        pass

                    decd, decm, decs, sign = 0.0, 0.0, 0.0, 1
                    decd = abs(float(decsplit[0]))
                    if decsplit[0][0] == '-':
                        sign = -1
                        pass
                    if len(decsplit) >= 2:
                        decm = float(decsplit[1])
                        pass
                    if len(decsplit) >= 3:
                        decs = float(decsplit[2])
                        pass
                    ra, dec = hms2rad(rah, ram, ras), dms2rad(decd, decm, decs, sign)
                    cat = ''
                    name = string.join(data[2:], ',')
                else:
                    print 'Position specification needs three part argument, separated by comma\'s: "ra,dec,caption"'
                    sys.exit(-1)
                    pass
                pass

            else:  # : in source
                index = 0
                cat = ''
                if source[0:2].upper() == '3C':
                    cat = '3C'
                    index = 2
                else:
                    for i in range(len(source)):
                        ch = source[i]
                        if ch.isalpha():
                            cat += ch
                        else:
                            index = i
                            break
                        pass  # for i...
                    pass

                if cat.upper() == 'N' or cat == '' or cat.upper == 'NGC':
                    cat = 'NGC'
                    pass

                if cat.upper() == 'I' or cat.upper() == 'IC':
                    cat = 'IC'
                    pass

                name = source[index:].upper().rstrip().lstrip()
                if cat == 'NGC' and name == '3690':
                    name = '3690A'
                    pass

                # determine ra, dec of fieldcentre
                ra = -1.0
                dec = 0.0
                if cat.upper() != 'M':
                    for niobj in deeplist:
                        if niobj.cat.upper() == cat.upper():
                            if name.upper() in niobj.all_names:
                                ra = niobj.ra
                                dec = niobj.dec
                                cat = niobj.cat
                                break
                            pass  # if niobj.cat
                        pass  # for niobj
                else:
                    cat = 'M'
                    for mobj in messierlist:
                        if mobj.messier == int(name):
                            ra = mobj.ra
                            dec = mobj.dec
                            name = str(mobj.messier)
                            break
                        pass  # for mobj
                    pass  # if cat == 'M'...

                pass

            print ''
            print cat, name

            if ra >= 0.0:
                artist = PDFDrawing(filename,
                                    settings.paperwidth,
                                    settings.paperwidth,
                                    font_metrics)

                sm = SkymapEngine(artist, font_metrics, settings.language, lm_stars=settings.limiting_magnitude_stars)
                sm.set_field(ra, dec, settings.fieldsize * pi / 180.0 / 2.0)
                caption = cat + ' ' + name

                if settings.caption is not False:
                    caption = settings.caption
                    pass
                if caption != '':
                    sm.set_caption(caption)
                    pass
                sm.make_map(starcatalog, deepskycatalog, settings.extra_positions_list)
            else:
                print 'object not found, try appending an A or a B'
                pass
            pass  # if source == 'allmessier'
        pass  # for source in sourcelist

    return open(filename)


def msort(x, y):
    r = 0
    if x.messier > y.messier:
        r = 1
    if x.messier < y.messier:
        r = -1
    return r
