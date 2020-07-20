
function retval = CalculateParameters (inputSpect)

% -------- vytvo�en� matice pro sou�et po 16 vzorc�ch

jednickovaM=zeros(16,rows(inputSpect));
step=1;
maxSize = columns(jednickovaM);

for radek=1:16
    for sloupec=step:step+15
      jednickovaM(radek, sloupec) = 1;
    endfor
    if(step+15 < maxSize) %kontrola, aby step nepokra�oval za velikost matice
    step = step + 16;
  endif
endfor

retval = jednickovaM * inputSpect; % v�sledek

endfunction
