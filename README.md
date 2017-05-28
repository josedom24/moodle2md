# moodle2md

## Objetivo

Convierte un curso moodle en un fichero plano escrito en Markdown que podemos subir a github.

## Características

Crea un directorio con un fichero `README.md` donde escribe los elementos del curso, un directorio `doc` donde guarda documentos markdown de las tareas y páginas que tiene el curso, un directorio `files` con los ficheros del curso y un directorio ìmg` donde guarda las imágenes.
Los recursos que convierte de un curso moodle son los siguientes:

* Títulos y comentarios de las secciones
* Label
* URL
* Resourse (ficheros ubidos al curso)
* Assign: La descripción de las tareas
* Page: Páginas

## ¿Cómo funciona?

Crea una copia de seguridad del curso que quieras exportar, descomprime el fichero que te has descargado. Para convertir el curso:

	$ python moodle2md -d <directorio copia moodle>

Se creará el directorio `course` con el curso exportado. si quiere indicar el directorio de salida:

	$ python moodle2md -d <directorio copia moodle> -o <directorio salida>

	