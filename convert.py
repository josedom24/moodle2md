from lxml import etree
import os,shutil
import unicodedata

DIR="course/"
FICHERO="README.md"

def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s


def borrar(fich,dir=DIR):
    f=open(dir+fich,"w")
    f.close()

def escribir(fich,texto="\n",dir=DIR):
    with open(dir+fich,"a") as fichero:
        fichero.write(texto.encode("utf-8"))
        if len(texto)>1 and texto[-1]!="\n":
            fichero.write("\n")

try:
    shutil.rmtree(DIR)
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
    
    os.mkdir("doc")
os.chdir("..")
borrar(FICHERO)

cursodoc=etree.parse('copia/course/course.xml')
titulo=cursodoc.find("fullname").text
descripcion=cursodoc.find("summary").text

doc = etree.parse('copia/moodle_backup.xml')

#titulo=doc.find("information/original_course_fullname").text
escribir(FICHERO,"# %s" % titulo)
escribir(FICHERO)

escribir(FICHERO,"# %s" % descripcion)
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
            nomfich=actividad.find("title").text.replace("/","_")
            nomfich=nomfich.replace(".","")+".md"
            nomfich=elimina_tildes(nomfich)
            borrar(nomfich,DIR+"doc/")
            if len(docassign.getroot())>0:
                for event in docassign.getroot():
                    escribir(nomfich,"# %s" % actividad.find("title").text,DIR+"doc/")
                    escribir(nomfich,event.find("description").text,DIR+"doc/")
            else:
                docassign=etree.parse("copia/%s/assign.xml" % actividad.find("directory").text)
                try:
                    escribir(nomfich,"# %s" % actividad.find("title").text,DIR+"doc/")
                    escribir(nomfich,docassign.find("assign/intro").text,DIR+"doc/")
                except:
                    pass
            escribir(FICHERO,"* [%s](%s)"%(actividad.find("title").text,"doc/"+nomfich))
        elif tipo=="resource":
            docresource=etree.parse("copia/%s/resource.xml" % actividad.find("directory").text)
            fileid=docresource.getroot().get("contextid")
            
            docfiles=etree.parse("copia/files.xml")
            fichero=docfiles.xpath("//file[contextid=%s]"%fileid)

            shutil.copyfile("copia/files/%s/%s"%(fichero[0].find("contenthash").text[0:2],fichero[0].find("contenthash").text),DIR+"files/%s"%fichero[0].find("filename").text) 
            escribir(FICHERO,"* [%s](%s)"%(actividad.find("title").text,"files/"+fichero[0].find("filename").text))
        elif tipo=="page":
            docpage=etree.parse("copia/%s/page.xml" % actividad.find("directory").text)    
            nomfich=actividad.find("title").text.replace(" ","_")
            nomfich=nomfich.replace("/","_")
            nomfich=nomfich.replace(".","")+".md"
            nomfich=elimina_tildes(nomfich)
            print nomfich
            borrar(nomfich,DIR+"doc/")
            try:
                escribir(nomfich,"# %s" % actividad.find("title").text,DIR+"doc/")
                escribir(nomfich,docpage.find("page/content").text,DIR+"doc/")
            except:
                pass
            escribir(FICHERO,"* [%s](%s)"%(actividad.find("title").text,"doc/"+nomfich))

        else:
            escribir(FICHERO, "* %s (%s)" % (actividad.find("title").text,actividad.find("modulename").text))

        print("* %s (%s)" % (actividad.find("title").text,actividad.find("modulename").text))