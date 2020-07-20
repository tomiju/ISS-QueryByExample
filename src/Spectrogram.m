
function retval = Spectrogram (input)

pkg load signal
[x,Fs] = audioread(input);
Fs = 16000; %frekvence
N = 512; % d�lka r�mce
wlen = 25e-3 * Fs; %d�lka sign�lu rozd�len� na r�mce
wshift = 10e-3*Fs; %posun mezi jednotliv�mi r�mci
woverlap = wlen - wshift; %p�ekryt� 15ms
win = hamming(wlen); %plot(win); %hammingovo okno o velikosti wlen
f = (0:(N/2-1)) / N * Fs; %dopln�n� do matice 
t = (0:(1 + floor((length(x) - wlen) / wshift) - 1))* wshift/Fs;  % minus one as of Matlab ...
X = specgram (x, N, Fs, win, woverlap); %vytvo�en� spectrogramu
imagesc(t,f,10*log(abs(X).^2)); # vykreslen�
set (gca (), "ydir", "normal"); xlabel ("Time");title('sx136.wav') ;ylabel ("Frequency [Hz]"); colormap(jet); # popisky os
retval = 10*log(abs(X).^2);
endfunction
