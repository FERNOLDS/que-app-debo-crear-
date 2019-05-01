#!/usr/bin/env python
# coding: utf-8

# # Perfiles de aplicaciones rentables para App Store y Google Play
# Nuestro objetivo en este proyecto es encontrar perfiles de aplicaciones móviles que sean rentables para los mercados App Store y Google Play. Estamos trabajando como analistas de datos para una compañía que crea aplicaciones móviles para Android y iOS, y nuestro trabajo es permitir que nuestro equipo de desarrolladores tome decisiones basadas en los datos con respecto al tipo de aplicaciones que crean.
# 
# En nuestra empresa, solo creamos aplicaciones que se pueden descargar e instalar de forma gratuita, y nuestra principal fuente de ingresos consiste en anuncios dentro de la aplicación. Esto significa que nuestros ingresos para cualquier aplicación dada están principalmente influenciados por el número de usuarios que usan nuestra aplicación. Nuestro objetivo para este proyecto es analizar los datos para ayudar a nuestros desarrolladores a comprender qué tipos de aplicaciones pueden atraer a más usuarios.
# 
# Abriendo y explorando los datos
# A partir de septiembre de 2018, había aproximadamente 2 millones de aplicaciones iOS disponibles en la App Store y 2.1 millones de aplicaciones Android en Google Play.
# 
# La recopilación de datos para más de cuatro millones de aplicaciones requiere una cantidad significativa de tiempo y dinero, por lo que intentaremos analizar una muestra de datos en su lugar. Para evitar gastar recursos en la recopilación de datos nuevos, primero debemos tratar de ver si podemos encontrar los datos existentes relevantes sin costo alguno. Afortunadamente, estos son dos conjuntos de datos que parecen adecuados para nuestro propósito:
# 
# Un conjunto de datos que contiene datos sobre aproximadamente diez mil aplicaciones de Android de Google Play
# Un conjunto de datos que contiene datos de aproximadamente siete mil aplicaciones iOS de la App Store
# Comencemos por abrir los dos conjuntos de datos y luego continuar con la exploración de los datos.

# In[1]:



from csv import reader

### The Google Play data set ###
opened_file = open('googleplaystore.csv')
read_file = reader(opened_file)
android = list(read_file)
android_header = android[0]
android = android[1:]

### The App Store data set ###
opened_file = open('AppleStore.csv')
read_file = reader(opened_file)
ios = list(read_file)
ios_header = ios[0]
ios = ios[1:]


# Para facilitar la exploración de los dos conjuntos de datos, primero escribiremos una función llamada explore_data () que podemos usar repetidamente para explorar filas de una manera más legible. También agregaremos una opción para que nuestra función muestre el número de filas y columnas para cualquier conjunto de datos.

# In[2]:


def explore_data(dataset, start, end, rows_and_columns=False):
    dataset_slice = dataset[start:end]    
    for row in dataset_slice:
        print(row)
        print('\n') # adds a new (empty) line between rows
        
    if rows_and_columns:
        print('Number of rows:', len(dataset))
        print('Number of columns:', len(dataset[0]))

print(android_header)
print('\n')
explore_data(android, 0, 3, True)


# In[3]:


print(ios_header)
print('\n')
explore_data(ios, 0, 3, True)


# # Eliminando datos malos
# 
# El conjunto de datos de Google Play tiene una sección de discusión dedicada, y podemos ver que una de las discusiones describe un error para la fila 1047

# In[4]:


print(android[10472])  # incorrect row
print('\n')
print(android_header)  # header
print('\n')
print(android[0])      # correct row


# 
# La fila 10472 corresponde a la aplicación Life Made WI-Fi Touchscreen Photo Frame, y podemos ver que la calificación es 19. Esto está claramente desactivado porque la calificación máxima para una aplicación de Google Play es 5. Como consecuencia, eliminaremos esta fil

# In[5]:


print(len(android))
del android[10472]  # don't run this more than once
print(len(android))


# # eliminando datos duplicados

# ## primera parte 

# revisando los datos duplicados nos damos cuenta de que uno de ellos es insatagram que tiene 4 entradas quepueden estar o no duplicadas

# In[6]:


for app in android:
    name = app[0]
    if name == 'Instagram':
        print(app)


# In[7]:


duplicate_apps = []
unique_apps = []

for app in android:
    name = app[0]
    if name in unique_apps:
        duplicate_apps.append(name)
    else:
        unique_apps.append(name)
    
print('Number of duplicate apps:', len(duplicate_apps))
print('\n')
print('Examples of duplicate apps:', duplicate_apps[:15])


# como podemos observar existen 1181 aplicaciones que estan duplicadas una vez o mas 

# para dejar solamente uno podriamos eliminar al azar pero eso seria poco profesional pero al hechar un vistazo podemos percatarnos que la cuarta columna difiere entre ellas y esta es el numero de opiniones.
# tomaremos a la fila que tenga mayor numero de opiniones para tener el mejor rating y para que sea mas confiable 

# ## segunda parte

# crearemos un diccionario en el cual esten todas las apps con el mayor numero de opiniones en caso de que se encuentren duplicadas para tener un nuevo diccionario sin tener apps duplicadas

# In[8]:


reviews_max = {}

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if name in reviews_max and reviews_max[name] < n_reviews:
        reviews_max[name] = n_reviews
        
    elif name not in reviews_max:
        reviews_max[name] = n_reviews


# para estar seguros de que la depuracion funciono haremos una simple resta entre el numero de apps inicial menos los 1181 apps duplicadas, esto deberia de darnos un nuevo diccionario con 9659 apps  

# In[9]:


print('Expected length:', len(android) - 1181)
print('Actual length:', len(reviews_max))


# pero tambien tenemos otro caso posible en el cual existan apps duplicadas que sean totalmente iguales es decir que el numero de opinianes sean iguales.
# para evitar que eso perjudique nuestro objetivo final, tendremos que realizar un nuevo diccionario

# In[10]:


android_clean = []
already_added = []

for app in android:
    name = app[0]
    n_reviews = float(app[3])
    
    if (reviews_max[name] == n_reviews) and (name not in already_added):
        android_clean.append(app)
        already_added.append(name)


# In[11]:



explore_data(android_clean, 0, 3, True)


# # Eliminando apps que no estan en ingles 

# para realizar la primera parte debemos de entender que las palabras o string "cadenas" son tambien un conjunto de datos separados es decir tu puedes dividir p-a-l-a-b-r-a cada letra"a" , etc tiene un numero asociado  que podemos verlo con la funcion ord 

# In[12]:


print(ord("a"))
print(ord("7"))


# como podemos ver todos las letras y simbolos tienen su propio numero, como si fuese su propio ID ahora segun la ASCII el rango para el idioma ingles es de 0 a 127, podriamos hacer loop en todos los lineas de nuestra base de datos limitando el numero de letras hasta 127, pero al revisar el codigo vimos que existen apps que llevan emojis y algunos caracteres especiales,
# por lo cual haremos que el depurador permita hasta 3 caracteres especiales 
# 

# In[13]:


def is_english(string):
    non_ascii = 0
    
    for character in string:
        if ord(character) > 127:
            non_ascii += 1
    
    if non_ascii > 3:
        return False
    else:
        return True

print(is_english('Docs To Go™ Free Office Suite'))
print(is_english('Instachat 😜'))


# el algoritmo puede que no funcione a la perfeccion pero con esto bastara hasta ahora

# In[14]:


android_english = []
ios_english = []

for app in android_clean:
    name = app[0]
    if is_english(name):
        android_english.append(app)
        
for app in ios:
    name = app[1]
    if is_english(name):
        ios_english.append(app)
        
explore_data(android_english, 0, 3, True)
print('\n')
explore_data(ios_english, 0, 3, True)


# arriba usamos la funcion is_english en la base de datos limpia de duplicados

# al ejecutar la funcion podemos ver que el numero de apps bajaron ya que se eliminaron las que estaban en un idioma que no ocupaba los caracteres del alfabeto ingles, puede ser que existan apps en espaniol  o cualquier otro idioma que ocupe un alfabeto similar al del english pero por ahora esta bien

#   # Aislando apps gratis

# In[15]:


android_final = []
ios_final = []

for app in android_english:
    price = app[7]
    if price == '0':
        android_final.append(app)
        
for app in ios_english:
    price = app[4]
    if price == '0.0':
        ios_final.append(app)
        
print(len(android_final))
print(len(ios_final))


# # Recordando el proposito del proyecto

# El proposito de este proyecto es encontrar las apps mas rentables y las que mas gustan a los usuarios, para que con esta informacion poder crear nuevas apps para los usuarios.
# primeramente tendremos que encontrar la mejor app en android y desarrollar para esa plataforma 
# despues des 6 meses, en caso de que la respuesta sea buena la desarrollaremos para IOS 
# como dijimos anteriormente nuestra empresa monetiza haciendo publicidad por ende necesitamos apps que tengan muchos usuarios.
# 

# In[16]:


def freq_table(dataset, index):
    table = {}
    total = 0
    
    for row in dataset:
        total += 1
        value = row[index]
        if value in table:
            table[value] += 1
        else:
            table[value] = 1
    
    table_percentages = {}
    for key in table:
        percentage = (table[key] / total) * 100
        table_percentages[key] = percentage 
    
    return table_percentages


def display_table(dataset, index):
    table = freq_table(dataset, index)
    table_display = []
    for key in table:
        key_val_as_tuple = (table[key], key)
        table_display.append(key_val_as_tuple)
        
    table_sorted = sorted(table_display, reverse = True)
    for entry in table_sorted:
        print(entry[1], ':', entry[0])


# In[17]:


display_table(ios_final, -5)


# In[18]:


display_table(android_final, 1) 


# In[19]:



display_table(android_final, -4)


# al correr el codigo se puede ver claramente cual es el porcentaje de applicaiones segun sus columnas

# # Apps mas populares segun su genero en App Store

# En la base de datos de Google Play pudimos clasificarlos y medirlos segun el numero de instalaciones, pero en la base de datos de IOS no podemos hacer eso ya que la base de datos no cuenta con esa informacion, pero podemos medirlo segun el rating y las opiniones que tiene. 

# In[20]:


genres_ios = freq_table(ios_final, -5)

for genre in genres_ios:
    total = 0
    len_genre = 0
    for app in ios_final:
        genre_app = app[-5]
        if genre_app == genre:            
            n_ratings = float(app[5])
            total += n_ratings
            len_genre += 1
    avg_n_ratings = total / len_genre
    print(genre, ':', avg_n_ratings)


# como podemos ver navegacion tiene un alto rating, pero esto es fuertemente influenciado debido a que Waze y Google Maps son quienes tienen cerca a medio millon de opiniones  

# In[21]:


for app in ios_final:
    if app[-5] == 'Navigation':
        print(app[1], ':', app[5]) 


# al igual que con navegacion, ocurre tambien con la categoria redes sociales que esta fuertemente influenciada por grandes como facebook, twiter, etc

# In[22]:


for app in ios_final:
    if app[-5] == 'Reference':
        print(app[1], ':', app[5])


# # Conclusion

# Segun lo investigado hasta ahora podemos concluir que las apps mas usadas son las de herramientas para el uso diario como ser Waze o las redes sociales, obviamente entrar a ese rubro y destronar a los reyes existentes es un trabajo super conplicado, pero no imposible, tambien se pueden hace mas filtraciones pero eso se debe hacer segun una meta especifica de la empresa o del data scientist, podriamos seguir nadando y encontrando nuevas informaciones importantes para otras empresas, que a nosotros no nos sirva por que no esta en nuestro foco. pero demostramos que se puede encontrar informacion para ponerse a trabajar.
# 
