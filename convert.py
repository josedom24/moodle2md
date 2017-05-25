from lxml import etree
import os
DIR="course/"
FICHERO="README.md"

def borrar(fich):
    f=open(DIR+fich,"w")
    f.close()

def escribir(fich,texto="\n"):
    with open(DIR+fich,"a") as fichero:
        fichero.write(texto.encode("utf-8"))
        if len(texto)>1 and texto[-1]!="\n":
            fichero.write("\n")

try:
    os.mkdir(DIR)
except:
    pass

borrar(FICHERO)
doc = etree.parse('copia/moodle_backup.xml')

titulo=doc.find("information/original_course_fullname").text
escribir(FICHERO,"# %s" % titulo)
escribir(FICHERO)

secciones=doc.find("information/contents/sections")
for seccion in secciones:
    docseccion=etree.parse("copia/%s/section.xml" % seccion.find("directory").text)
    summary=docseccion.find("summary").text
    summary=summary.split(">")[1].split("<")[0]
    if len(summary)>0 and summary[0]=="\n":
        summary=summary[1:]
    if len(summary)>0:
        escribir(FICHERO)
        escribir(FICHERO,"## %s"%summary)
        escribir(FICHERO)
    sectionid=seccion.find("sectionid").text
    actividades=doc.xpath("//activity[sectionid=%s]"%sectionid)
    for actividad in actividades:
        tipo = actividad.find("modulename").text
        if tipo=="label":
            escribir(FICHERO)
            escribir(FICHERO,"#### %s" % actividad.find("title").text)
            escribir(FICHERO)
        elif tipo=="url":
            docactivity=etree.parse("copia/%s/url.xml" % actividad.find("directory").text)
            escribir(FICHERO, "* [%s](%s)"%(actividad.find("title").text,docactivity.find("url/externalurl").text))
        else:
            escribir(FICHERO, "* %s (%s)" % (actividad.find("title").text,actividad.find("modulename").text))
