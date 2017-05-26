from lxml import etree
import os,shutil
DIR="course/"
FICHERO="README.md"

def borrar(fich,dir=DIR):
    f=open(dir+fich,"w")
    f.close()

def escribir(fich,texto="\n",dir=DIR):
    with open(dir+fich,"a") as fichero:
        fichero.write(texto.encode("utf-8"))
        if len(texto)>1 and texto[-1]!="\n":
            fichero.write("\n")

try:
    os.mkdir(DIR)
except:
    pass

try:
    os.chdir(DIR)
    os.mkdir("files")
except:
    os.rmdir("files")
    os.mkdir("files")
try:
    os.mkdir("doc")
except:
    shutil.rmtree("doc")
    os.mkdir("doc")
os.chdir("..")
borrar(FICHERO)
doc = etree.parse('copia/moodle_backup.xml')

titulo=doc.find("information/original_course_fullname").text
escribir(FICHERO,"# %s" % titulo)
escribir(FICHERO)

secciones=doc.find("information/contents/sections")
for seccion in secciones:
    docseccion=etree.parse("copia/%s/section.xml" % seccion.find("directory").text)
    summary=docseccion.find("summary").text

    #summary=summary.split(">")[1].split("<")[0]
    try:
        if len(summary)>0 and summary[0]=="\n":
            summary=summary[1:]
        if len(summary)>0:
            escribir(FICHERO)
            escribir(FICHERO,"## %s"%summary)
            escribir(FICHERO)
    except:
        pass
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
        elif tipo=="assign":
            docassign=etree.parse("copia/%s/calendar.xml" % actividad.find("directory").text)
            nomfich=actividad.find("title").text.replace(" ","_")
            nomfich=nomfich.replace(".","")+".md"
            borrar(nomfich,DIR+"doc/")
            if len(docassign.getroot())>0:
                for event in docassign.getroot():
                    escribir(nomfich,event.find("description").text,DIR+"doc/")
            else:
                docassign=etree.parse("copia/%s/assign.xml" % actividad.find("directory").text)
                try:
                    escribir(nomfich,docassign.find("assign/intro").text,DIR+"doc/")
                except:
                    pass
            escribir(FICHERO,"* [%s](%s)"%(actividad.find("title").text,"doc/"+nomfich))

        else:
            escribir(FICHERO, "* %s (%s)" % (actividad.find("title").text,actividad.find("modulename").text))