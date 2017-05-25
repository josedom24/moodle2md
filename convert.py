from lxml import etree

doc = etree.parse('copia/moodle_backup.xml')

titulo=doc.find("information/original_course_fullname").text
print "# %s" % titulo
print

secciones=doc.find("information/contents/sections")
for seccion in secciones:
    docseccion=etree.parse("copia/%s/section.xml" % seccion.find("directory").text)
    summary=docseccion.find("summary").text
    summary=summary.split(">")[1].split("<")[0]
    if len(summary)>0 and summary[0]=="\n":
        summary=summary[1:]
    if len(summary)>0:
        print
        print "## %s"%summary
        print
    sectionid=seccion.find("sectionid").text
    actividades=doc.xpath("//activity[sectionid=%s]"%sectionid)
    for actividad in actividades:
        tipo = actividad.find("modulename").text
        if tipo=="label":
            print
            print "#### %s" % actividad.find("title").text
            print
        elif tipo=="url":
            docactivity=etree.parse("copia/%s/url.xml" % actividad.find("directory").text)
            print
            print "* [%s](%s)"%(actividad.find("title").text,docactivity.find("url/externalurl").text)
            print
        else:
            print "* %s (%s)" % (actividad.find("title").text,actividad.find("modulename").text)
