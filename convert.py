#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import etree
import os,shutil
import unicodedata

DIR="course/"
FICHERO="README.md"

def getNombreFichero(nombre):
    nombre=elimina_tildes(nombre)
    nombre=elimina_caracteres_nombre_fichero(nombre)
    return nombre+".md"

def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',unicode(cadena)) if unicodedata.category(c) != 'Mn'))
    return s

def elimina_caracteres_nombre_fichero(nomfich):
    car=("/","?","(",")"," ")
    for c in car:
        nomfich=nomfich.replace(c,"_")
    return nomfich


def escribir(fich,texto="\n",dir=DIR):
    with open(dir+fich,"a") as fichero:
        fichero.write(texto.encode("utf-8"))
        if len(texto)>1 and texto[-1]!="\n":
            fichero.write("\n")

def images(html):
    html= html.replace("$@FILEPHP@$$@SLASH@$img$@SLASH@$","img/")
    html= html.replace("$@FILEPHP@$$@SLASH@$","../img/")
    return html


def copiar_imagenes():
    filesdoc=etree.parse('copia/files.xml')
    imagenes=filesdoc.xpath("//file/filename[contains(text(),'.jpg') or contains(text(),'.png')  or contains(text(),'.gif') ]/..")
    for img in imagenes:
        shutil.copyfile("copia/files/%s/%s"%(img.find("contenthash").text[0:2],img.find("contenthash").text),DIR+"img/%s"%img.find("filename").text) 



def crear_directorios():
    try:
        shutil.rmtree(DIR)
        os.mkdir(DIR)
    except:
        pass    

    try:
        os.chdir(DIR)
        os.mkdir("files")
        os.mkdir("doc")
        os.mkdir("img")
    except:
        pass
    os.chdir("..")

def getTituloDescripcion():
    cursodoc=etree.parse('copia/course/course.xml')
    titulo=cursodoc.find("fullname").text
    descripcion=cursodoc.find("summary").text
    escribir(FICHERO,"# %s" % titulo)
    escribir(FICHERO)
    escribir(FICHERO,"# %s" % descripcion)
    escribir(FICHERO)

def getSeccionesActividades():

    doc = etree.parse('copia/moodle_backup.xml')
    secciones=doc.find("information/contents/sections")
    for seccion in secciones:
        docseccion=etree.parse("copia/%s/section.xml" % seccion.find("directory").text)
        summary=docseccion.find("summary").text

        try:
            if len(summary)>0 and summary[0]=="\n":
                summary=summary[1:]
            if len(summary)>0:
                escribir(FICHERO)
                escribir(FICHERO,"## %s"%images(summary))
                escribir(FICHERO)
        except:
            pass
        sectionid=seccion.find("sectionid").text
        actividades=doc.xpath("//activity[sectionid=%s]"%sectionid)
        for actividad in actividades:
            tipo = actividad.find("modulename").text
            if tipo=="label":
                getLabel(actividad)
            elif tipo=="url":
                getUrl(actividad)
            elif tipo=="assign":
                getAssign(actividad)
            elif tipo=="resource":
                getResource(actividad)
            elif tipo=="page":
                getPage(actividad)  
            else:
                escribir(FICHERO, "* %s (%s)" % (actividad.find("title").text,actividad.find("modulename").text))

def getLabel(actividad):
    doclabel=etree.parse("copia/%s/label.xml" % actividad.find("directory").text)
    escribir(FICHERO)
    escribir(FICHERO,"#### %s" % images(doclabel.find("label/intro").text))
    escribir(FICHERO)

def getUrl(actividad):
    docactivity=etree.parse("copia/%s/url.xml" % actividad.find("directory").text)
    escribir(FICHERO, "* [%s](%s)"%(actividad.find("title").text,docactivity.find("url/externalurl").text))

def getAssign(actividad):
    docassign=etree.parse("copia/%s/calendar.xml" % actividad.find("directory").text)
    nomfich=getNombreFichero(actividad.find("title").text)
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

def getResource(actividad):
    docresource=etree.parse("copia/%s/resource.xml" % actividad.find("directory").text)
    fileid=docresource.getroot().get("contextid")
    docfiles=etree.parse("copia/files.xml")
    fichero=docfiles.xpath("//file[contextid=%s]"%fileid)   
    shutil.copyfile("copia/files/%s/%s"%(fichero[0].find("contenthash").text[0:2],fichero[0].find("contenthash").text),DIR+"files/%s"%fichero[0].find("filename").text) 
    escribir(FICHERO,"* [%s](%s)"%(actividad.find("title").text,"files/"+fichero[0].find("filename").text))

def getPage(actividad):
    docpage=etree.parse("copia/%s/page.xml" % actividad.find("directory").text)    
    nomfich=getNombreFichero(actividad.find("title").text)
    try:
        escribir(nomfich,"# %s" % actividad.find("title").text,DIR+"doc/")
        escribir(nomfich,images(docpage.find("page/content").text),DIR+"doc/")
    except:
        pass
    escribir(FICHERO,"* [%s](%s)"%(actividad.find("title").text,"doc/"+nomfich))  


if __name__ == '__main__':
    crear_directorios()
    copiar_imagenes()
    getTituloDescripcion()
    getSeccionesActividades()



