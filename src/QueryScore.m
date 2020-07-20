
function retval = QueryScore (queryM, sentenceM)
  
total_steps = columns(sentenceM)-columns(queryM); # maxim�ln� po�et krok� - nesm�m j�t mimo hranice 
resultVect = zeros(1,columns(sentenceM)); # vektor pro v�sledky korelace

for i = 1:total_steps # i = pp ze zad�n�
    pomKorelace=QueryPom(queryM, sentenceM, i); # pro ka�d� "pp" po��t�m korelaci pomoc� fce corr
    resultVect(i)=pomKorelace; # v�sledky ukl�d�m
endfor

retval = resultVect;
endfunction
