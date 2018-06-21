#!/usr/bin/env python
# -*- coding: utf-8 -*-
from lxml import etree
from sys import argv
import os,shutil
import unicodedata
import argparse
import zipfile



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

def crear_fichero(fich,dir):
    f=open(dir+fich,"w")
    f.close()

def escribir(dir,fich,texto="\n"):
    with open(dir+fich,"a") as fichero:
        fichero.write(texto.encode("utf-8"))
        if len(texto)>1 and texto[-1]!="\n":
            fichero.write("\n")

def images(html):
    html= html.replace("$@FILEPHP@$$@SLASH@$img$@SLASH@$","img/")
    html= html.replace("$@FILEPHP@$$@SLASH@$","../img/")
    return html


def copiar_imagenes(DIR_COPIA,DIR):
    filesdoc=etree.parse(DIR_COPIA+"/files.xml")
    imagenes=filesdoc.xpath("//file/filename[contains(text(),'.jpg') or contains(text(),'.png')  or contains(text(),'.gif') ]/..")
    for img in imagenes:
        shutil.copyfile(DIR_COPIA+"/files/%s/%s"%(img.find("contenthash").text[0:2],img.find("contenthash").text),DIR+"img/%s"%img.find("filename").text) 



def crear_directorios(DIR,FICHERO):
    try:
        shutil.rmtree(DIR)
    except:
        pass    
    try:
        os.mkdir(DIR)
        crear_fichero(FICHERO,DIR)
    except:
        raise OSError
    
    try:
        os.chdir(DIR)
        os.mkdir("files")
        os.mkdir("doc")
        os.mkdir("img")
    except:
        pass
    os.chdir("..")

def getTituloDescripcion(DIR_COPIA,DIR,FICHERO):
    cursodoc=etree.parse(DIR_COPIA+'/course/course.xml')
    titulo=cursodoc.find("fullname").text
    descripcion=cursodoc.find("summary").text
    escribir(DIR,FICHERO,"# %s" % titulo)
    escribir(DIR,FICHERO)
    escribir(DIR,FICHERO,"# %s" % descripcion)
    escribir(DIR,FICHERO)

def getSeccionesActividades(DIR_COPIA,DIR,FICHERO):

    doc = etree.parse(DIR_COPIA+'/moodle_backup.xml')
    secciones=doc.find("information/contents/sections")
    for seccion in secciones:
        docseccion=etree.parse(DIR_COPIA+"/%s/section.xml" % seccion.find("directory").text)
        summary=docseccion.find("summary").text

        try:
            if len(summary)>0 and summary[0]=="\n":
                summary=summary[1:]
            if len(summary)>0:
                escribir(DIR,FICHERO)
                escribir(DIR,FICHERO,"## %s"%images(summary))
                escribir(DIR,FICHERO)
        except:
            pass
        sectionid=seccion.find("sectionid").text
        actividades=doc.xpath("//activity[sectionid=%s]"%sectionid)
        for actividad in actividades:
            tipo = actividad.find("modulename").text
            if tipo=="label":
                getLabel(actividad,DIR_COPIA,DIR,FICHERO)
            elif tipo=="url":
                getUrl(actividad,DIR_COPIA,DIR,FICHERO)
            elif tipo=="assign":
                getAssign(actividad,DIR_COPIA,DIR,FICHERO)
            elif tipo=="resource":
                getResource(actividad,DIR_COPIA,DIR,FICHERO)
            elif tipo=="page":
                getPage(actividad,DIR_COPIA,DIR,FICHERO)  
            else:
                escribir(DIR,FICHERO, "* %s (%s)" % (actividad.find("title").text,actividad.find("modulename").text))

def getLabel(actividad,DIR_COPIA,DIR,FICHERO):
    doclabel=etree.parse(DIR_COPIA+"/%s/label.xml" % actividad.find("directory").text)
    escribir(DIR,FICHERO)
    escribir(DIR,FICHERO,"#### %s" % images(doclabel.find("label/intro").text))
    escribir(DIR,FICHERO)

def getUrl(actividad,DIR_COPIA,DIR,FICHERO):
    docactivity=etree.parse(DIR_COPIA+"/%s/url.xml" % actividad.find("directory").text)
    escribir(DIR,FICHERO, "* [%s](%s)"%(actividad.find("title").text,docactivity.find("url/externalurl").text))

def getAssign(actividad,DIR_COPIA,DIR,FICHERO):
    docassign=etree.parse(DIR_COPIA+"/%s/calendar.xml" % actividad.find("directory").text)
    nomfich=getNombreFichero(actividad.find("title").text)
    if len(docassign.getroot())>0:
        for event in docassign.getroot():
            escribir(DIR+"doc/",nomfich,"# %s" % actividad.find("title").text)
            escribir(DIR+"doc/",nomfich,event.find("description").text)
    else:
        docassign=etree.parse(DIR_COPIA+"/%s/assign.xml" % actividad.find("directory").text)
        try:
            escribir(DIR+"doc/",nomfich,"# %s" % actividad.find("title").text)
            escribir(DIR+"doc/",nomfich,docassign.find("assign/intro").text)
        except:
            pass
    escribir(DIR,FICHERO,"* [%s](%s)"%(actividad.find("title").text,"doc/"+nomfich))    

def getResource(actividad,DIR_COPIA,DIR,FICHERO):
    docresource=etree.parse(DIR_COPIA+"/%s/resource.xml" % actividad.find("directory").text)
    fileid=docresource.getroot().get("contextid")
    docfiles=etree.parse(DIR_COPIA+"/files.xml")
    fichero=docfiles.xpath("//file[contextid=%s]"%fileid)   
    try:
        shutil.copyfile(DIR_COPIA+"/files/%s/%s"%(fichero[0].find("contenthash").text[0:2],fichero[0].find("contenthash").text),DIR+"files/%s"%fichero[0].find("filename").text) 
        escribir(DIR,FICHERO,"* [%s](%s)"%(actividad.find("title").text,"files/"+fichero[0].find("filename").text))
    except:
        print "Fichero no encontrado."
        print actividad.find("directory").text,fileid

def getPage(actividad,DIR_COPIA,DIR,FICHERO):
    docpage=etree.parse(DIR_COPIA+"/%s/page.xml" % actividad.find("directory").text)    
    nomfich=getNombreFichero(actividad.find("title").text)
    try:
        escribir(DIR+"doc/",nomfich,"# %s" % actividad.find("title").text)
        escribir(DIR+"doc/",nomfich,images(docpage.find("page/content").text))
    except:
        pass
    escribir(DIR,FICHERO,"* [%s](%s)"%(actividad.find("title").text,"doc/"+nomfich))


def main():
    
    parser = argparse.ArgumentParser(description='Convierte curso moodle a Markdown')
    parser.add_argument('-d',  type=str, required=True, help='directorio curso moodle')
    parser.add_argument('-o',  type=str, help='directorio de salida')
    #parser.add_argument('-o', 
     #              help='sum the integers (default: find the max)')
    args = parser.parse_args()
    DIR_COPIA=args.d
    if args.o!=None:
        DIR=args.o+"/"
    else:
        DIR="course/"
    FICHERO="README.md"
    crear_directorios(DIR,FICHERO)
    copiar_imagenes(DIR_COPIA,DIR)
    getTituloDescripcion(DIR_COPIA,DIR,FICHERO)
    getSeccionesActividades(DIR_COPIA,DIR,FICHERO)



if __name__ == '__main__':
    main()
    

        



