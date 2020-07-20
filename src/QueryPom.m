
function retval = QueryPom (queryM, sentenceM, i)

korelaceVysledek=0; # výsledek korelace pro aktuální "pp"
pom=0; # pomocná promìnná pro výpoèet korelací

for sloupec = 1:columns(queryM) 
 pom=corr(queryM(1:16, [sloupec]), sentenceM(1:16, [sloupec + i])); # výpoèet korelace pomocí funkce "corr"
 korelaceVysledek += pom;    
endfor

retval=korelaceVysledek / columns(queryM); # výsledek chci mezi -1 a 1, tudíž musím hodnotu normalizovat

endfunction

