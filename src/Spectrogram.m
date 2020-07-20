
function retval = Spectrogram (input)

pkg load signal
[x,Fs] = audioread(input);
Fs = 16000; %frekvence
N = 512; % délka rámce
wlen = 25e-3 * Fs; %délka signálu rozdìlená na rámce
wshift = 10e-3*Fs; %posun mezi jednotlivými rámci
woverlap = wlen - wshift; %pøekrytí 15ms
win = hamming(wlen); %plot(win); %hammingovo okno o velikosti wlen
f = (0:(N/2-1)) / N * Fs; %doplnìní do matice 
t = (0:(1 + floor((length(x) - wlen) / wshift) - 1))* wshift/Fs;  % minus one as of Matlab ...
X = specgram (x, N, Fs, win, woverlap); %vytvoøení spectrogramu
imagesc(t,f,10*log(abs(X).^2)); # vykreslení
set (gca (), "ydir", "normal"); xlabel ("Time");title('sx136.wav') ;ylabel ("Frequency [Hz]"); colormap(jet); # popisky os
retval = 10*log(abs(X).^2);
endfunction
