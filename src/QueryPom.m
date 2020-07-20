
function retval = QueryPom (queryM, sentenceM, i)

korelaceVysledek=0; # v�sledek korelace pro aktu�ln� "pp"
pom=0; # pomocn� prom�nn� pro v�po�et korelac�

for sloupec = 1:columns(queryM) 
 pom=corr(queryM(1:16, [sloupec]), sentenceM(1:16, [sloupec + i])); # v�po�et korelace pomoc� funkce "corr"
 korelaceVysledek += pom;    
endfor

retval=korelaceVysledek / columns(queryM); # v�sledek chci mezi -1 a 1, tud� mus�m hodnotu normalizovat

endfunction

