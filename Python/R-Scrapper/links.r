### Getting links

library(stringr)
library(rvest)

pag<-"s?k=aspiradora&page=2&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&qid=1559659201&ref=sr_pg_2"
lista_paginas<-c(1:10)
pag<-str_replace(pag, "page=2", paste0("page=",lista_paginas))
pag<-str_replace(pag, "sr_pg_2", paste0("sr_pg_",lista_paginas))
paginas<-paste0("https://www.amazon.es/", pag)

dameLinksPagina<-function(url){
  selector<-"div > div:nth-child(1) > div > div > div:nth-child(1) > h2 > a"
  pagina<-read_html(url)
  nodo<-html_nodes(pagina, selector)
  nodo_text<-html_text(nodo)
  nodo_links<-html_attr(nodo, "href")
  nodo_links
  
}

linksAsp<-sapply(paginas, dameLinksPagina)
vlink<-as.vector(linksAsp)
vlink<- vlink[!(nchar(vlink)==12)]

vlinkAspiradora<-paste0("https://www.amazon.es/", vlink)


### Obtaining data from each link

getArticulo <- function(url){
    
    pagina_web <- read_html(url)

    nombre <- "#productTitle"
    nombre_nodo <- html_node(pagina_web, nombre)
    nombre_texto <- html_text(nombre_nodo)
    nombre_texto
    
    
    opiniones <- "#acrCustomerReviewText"
    opiniones_nodo <- html_node(pagina_web, opiniones)
    opiniones_texto <- html_text(opiniones_nodo)
    opiniones_texto
    
    
    precio <- "#priceblock_ourprice"
    precio_nodo <- html_node(pagina_web, precio)
    precio_texto <- html_text(precio_nodo)
    precio_texto
    
    
    tabla <- "#prodDetails > div > div.column.col1 > div > div.content.pdClearfix > div > div > table"
    tabla_nodo <- html_node(pagina_web, tabla)
    
    col <- c("Peso del producto","Dimensiones del producto","Volumen","Potencia")
    
    if(!is.na(tabla_nodo)){
        
        tabla_texto <- html_table(tabla_nodo)
    
        val <- tabla_texto$X2
        res_tabla <- data.frame(t(val))

        tabla_name <-tabla_texto$X1
        colnames(res_tabla) <- tabla_name
        
        zero <- matrix("-1", ncol = 4, nrow = 1)
        dfzero <- as.data.frame(zero)
        colnames(dfzero) <- col
        
        peso <- as.character(res_tabla$`Peso del producto`)
        if(length(peso)==0) peso <- "-1"
        
        dime <- as.character(res_tabla$`Dimensiones del producto`)
        if(length(dime)==0) dime <- "-1"
        
        potencia <- as.character(res_tabla$`Potencia`)
        if(length(potencia)==0) potencia <- "-1"
        
        volumen <- as.character(res_tabla$`Volumen`)
        if(length(volumen)==0) volumen <- "-1"
        
        #Una vez comprobados los valores, si asignan al dataframe de -1 creado
        dfzero$`Peso del producto` <- peso
        dfzero$`Dimensiones del producto` <- dime
        dfzero$`Potencia` <- potencia
        dfzero$`Volumen` <- volumen
        
        mitab <- dfzero
        colnames(mitab) <- col
    
    }else{
        
        mitab <- data.frame(colnames(col))
        mitab <- rbind(mitab, c("-1","-1","-1","-1"))
        colnames(mitab) <- col 
    }
   
    
   articulo <- c(nombre_texto,precio_texto,opiniones_texto,
                           as.character(mitab$'Peso del producto'[1]),
                           as.character(mitab$'Dimensiones del producto'),
                           as.character(mitab$'Volumen'),
                           as.character(mitab$'Potencia'))
    articulo

}


### Dataprocessing

resultado_datos <- sapply(vlinkAspiradora,getArticulo)
res <- t(resultado_datos)
colnames(res) <- c('Nombre','Precio','Opiniones','Peso del producto','Dimensiones del producto','Volumen','Potencia')
rownames(res) <- c(1:200)
res <- res[complete.cases(res), ]
vacuum <- as.data.frame(res)

#Peso del producto
vacuum$'Peso del producto' <- as.character(vacuum$'Peso del producto')
vacuum$'Peso del producto' <- gsub(' Kg','',vacuum$'Peso del producto')
vacuum$'Peso del producto' <- gsub(',','.',vacuum$'Peso del producto')
vacuum$'Peso del producto' <- gsub('-1',NA,vacuum$'Peso del producto')
vacuum$'Peso del producto' <- as.numeric(vacuum$'Peso del producto')

pesomedio <- mean(vacuum$'Peso del producto', na.rm=TRUE)
vacuum$'Peso del producto'[is.na(vacuum$'Peso del producto')] <- pesomedio

#Volumen
vacuum$'Volumen' <- as.character(vacuum$'Volumen')
vacuum$'Volumen' <- gsub(' litros','',vacuum$'Volumen')
vacuum$'Volumen' <- gsub('-1',NA,vacuum$'Volumen')
vacuum$'Volumen' <- as.numeric(vacuum$'Volumen')

volmedio <- mean(vacuum$'Volumen', na.rm=TRUE)
vacuum$'Volumen'[is.na(vacuum$'Volumen')] <- volmedio

#Potencia
vacuum$'Potencia' <- as.character(vacuum$'Potencia')
vacuum$'Potencia' <- gsub(' vatios','',vacuum$'Potencia')
vacuum$'Potencia' <- gsub('-1',NA,vacuum$'Potencia')
vacuum$'Potencia' <- as.numeric(vacuum$'Potencia')

potmedio <- mean(vacuum$'Potencia', na.rm=TRUE)
vacuum$'Potencia'[is.na(vacuum$'Potencia')] <- potmedio

#Opiniones
vacuum$'Opiniones' <- as.character(vacuum$'Opiniones')
vacuum$'Opiniones' <- gsub(' valoraciones','',vacuum$'Opiniones')
vacuum$'Opiniones' <- gsub(' valoración','',vacuum$'Opiniones')
vacuum$'Opiniones' <- gsub('.','',vacuum$'Opiniones',fixed = T)
vacuum$'Opiniones' <- as.numeric(vacuum$'Opiniones')


#Precio
vacuum$'Precio' <- as.character(vacuum$'Precio')
vacuum$'Precio' <- gsub("€", "", vacuum$'Precio', fixed = TRUE)
vacuum$'Precio' <- gsub(',','.',vacuum$'Precio')
vacuum$'Precio' = substr(vacuum$'Precio',1,nchar(vacuum$'Precio')-1)
vacuum$'Precio' <- as.numeric(vacuum$'Precio')

#Dimensiones
vacuum$'Dimensiones del producto' <- as.character(vacuum$'Dimensiones del producto')
vacuum$'Dimensiones del producto' <- gsub("cm", "", vacuum$'Dimensiones del producto', fixed = TRUE)
vacuum$'Dimensiones del producto' <- gsub(",", ".", vacuum$'Dimensiones del producto', fixed = TRUE)
vacuum$'Dimensiones del producto' = substr(vacuum$'Dimensiones del producto',1,nchar(vacuum$'Dimensiones del producto')-1)

    #Trabajando las dimensiones

    dimen <- str_split_fixed(vacuum$'Dimensiones del producto'," x ", n=3)

    dim_1 <- dimen[,1]
    dim_1 <- as.numeric(dim_1)
    dim_1_mean <- mean(dim_1, na.rm=TRUE)
    dim_1[is.na(dim_1)] <- dim_1_mean

    dim_2 <- dimen[,2]
    dim_2 <- as.numeric(dim_2)
    dim_2_mean <- mean(dim_2, na.rm=TRUE)
    dim_2[is.na(dim_2)] <- dim_2_mean

    dim_3 <- dimen[,3]
    dim_3 <- as.numeric(dim_3)
    dim_3_mean <- mean(dim_3, na.rm=TRUE)
    dim_3[is.na(dim_3)] <- dim_3_mean

    dimensions <- data.frame(dim_1, dim_2, dim_3)
    colnames(dimensions) <- c("Alto","Ancho","Profundo")

    vacuum <- cbind(vacuum, dimensions)
    vacuum$'Dimensiones del producto' <- NULL

vacumm