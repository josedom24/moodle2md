from lxml import etree

doc = etree.parse('copia/moodle_backup.xml')

titulo=doc.find("information/original_course_fullname").text
print "# %s" % titulo

secciones=doc.find("information/contents/sections")
for seccion in secciones:
    docseccion=etree.parse("copia/%s/section.xml" % seccion.find("directory").text)
    summary=docseccion.find("summary").text
    summary=summary.split(">")[1].split("<")[0]
    if len(summary)>0 and summary[0]=="\n":
        summary=summary[1:]
    if len(summary)>0:
        print "## %s"%summary
