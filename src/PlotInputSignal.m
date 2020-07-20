
function retval = PlotInputSignal (input)
# todo
[x,Fs] = audioread(input);
t=linspace(0, length(x)/Fs, length(x));
plot(t,x)

endfunction
