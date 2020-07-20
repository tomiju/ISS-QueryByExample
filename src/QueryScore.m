
function retval = QueryScore (queryM, sentenceM)
  
total_steps = columns(sentenceM)-columns(queryM); # maximální poèet krokù - nesmím jít mimo hranice 
resultVect = zeros(1,columns(sentenceM)); # vektor pro výsledky korelace

for i = 1:total_steps # i = pp ze zadání
    pomKorelace=QueryPom(queryM, sentenceM, i); # pro každé "pp" poèítám korelaci pomocí fce corr
    resultVect(i)=pomKorelace; # výsledky ukládám
endfor

retval = resultVect;
endfunction
