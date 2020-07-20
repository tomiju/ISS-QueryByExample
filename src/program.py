import numpy as np
import matplotlib.pyplot as plt
import soundfile as sf
from scipy.signal import spectrogram, lfilter, freqz, tf2zpk
import scipy
import scipy.stats
from scipy import stats
from pydub import AudioSegment
import sys

np.set_printoptions(threshold=sys.maxsize)

#------------------------------------------------------------------

# Funkce pro načtení vstupního .wav souboru
def LoadInput(inputFile):
    s, fs = sf.read(inputFile)
    t = np.arange(s.size) / fs
    
    return s, fs, t

# Funkce pro výpočet spektrogramu
def Spectrogram(fs, s):
    
    wlen = 25 * fs // 1000
    wshift = 10 * fs // 1000
    woverlap = wlen - wshift
    nperseg = 25 * fs  // 1000 
    f, t, sgr = spectrogram(s, fs, noverlap=woverlap, nperseg=nperseg, nfft=511)
    
    sgr_log = 10 * np.log10(sgr+1e-20) # matice "X"
    
    return sgr_log, f, t

# Funkce pro přípravu pomocné matice a následného vypočítání hodnot parametrů
def CalculateParameters(inputMatrix):

    jednickovaM = np.zeros((16,len(inputMatrix)))
    
    for radek in range(16):
     for sloupec in range(radek*16, radek*16+16):
        jednickovaM[radek][sloupec] = 1
        
        
    F = np.dot(jednickovaM, inputMatrix)
    
    return F
 
# Pomocná funkce pro výpočet hodnoty skóre    
def QueryPom(F, Q, pp):
    
    pom = 0 
    
    for i in range(Q[0].shape[0]):
        pom_korelace, p_value = stats.pearsonr(Q[:,i], F[:,i + pp])
        pom += pom_korelace
        
    return pom / Q[0].shape[0]

# Funkce pro výpočet hodnoty skóre (korelace)
def QueryScore(F, Q):

    F_length = F[0].shape[0]
    Q_length = Q[0].shape[0]

    max_size = F_length - Q_length
    correlations_vector = np.zeros(F_length)
    
    for i in range(max_size):
        pom_korelace = QueryPom(F, Q, i)
        correlations_vector[i] = pom_korelace

    return correlations_vector

#------------------------------------------------------------------

inputFileS = '../sentences/sx136.wav' # input file
inputF = 'sx136.wav' # input file jméno pro vykreslení
inputFileQ1 = '../queries/q1.wav'
inputFileQ2 = '../queries/q2.wav'


# Načtení vstupních .wav souborů
s, fs, t = LoadInput(inputFileS)

#--------------------------------------------------
# Kreslení grafů
plt.figure(figsize=(12,7))
plt.subplot(311)
plt.subplots_adjust(left=None, bottom=-0.7, right=None, top=0.9, wspace=None, hspace=None)
plt.gca().set_xlabel('$t$')
plt.gca().set_ylabel('signal')
plt.gca().set_title('"scientific" and "development" vs "'+inputF +'"', fontweight="bold")
plt.plot(t, s)
plt.margins(0)
#--------------------------------------------------

# Načtení vstupních .wav souborů
s1, fs1, t1 = LoadInput(inputFileQ1)
s2, fs2, t2 = LoadInput(inputFileQ2)

# Spektrogram
F_input, f11, t11 = Spectrogram(fs, s)

"""#--------------------------------------------------
# Kreslení grafů
plt.subplot(312)
plt.pcolormesh(t11,f11/1000,F_input)
plt.gca().set_xlabel('$t[s]$')
plt.gca().set_ylabel('features')
plt.margins(0)
#--------------------------------------------------"""

# Spektrogram
Q1_input, f_null, t_null = Spectrogram(fs1, s1)
Q2_input, f_null, t_null = Spectrogram(fs2, s2)

# Výpočet hodnot parametrů (features)
F = CalculateParameters(F_input)
Q1 = CalculateParameters(Q1_input)
Q2 = CalculateParameters(Q2_input)

#--------------------------------------------------
# Kreslení grafů
import matplotlib.ticker as ticker
plt.subplot(312)
plt.pcolormesh(F)
ticks_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/100))
plt.gca().xaxis.set_major_formatter(ticks_x)
plt.gca().invert_yaxis()
plt.gca().set_xlabel('$t$')
plt.gca().set_ylabel('features')
plt.margins(0)
#--------------------------------------------------

# Výpočet skóre (korelace) query se vstupní větou
scoreQ1 = QueryScore(F, Q1)
scoreQ2 = QueryScore(F, Q2)

#--------------------------------------------------
# Kreslení grafů
plt.subplot(313)
t = np.arange(scoreQ2.size) / 100 #/ fs * 360 / 2
plt.plot(t, scoreQ2, label='development')
t = np.arange(scoreQ1.size) / 100 #/ fs * 360 / 2 #* fs/1000000
plt.plot(t, scoreQ1, label='scientific')
axes = plt.gca()
axes.set_ylim([0,1])
axes.set_ylabel('scores')
plt.gca().set_xlabel('$t$');
plt.margins(0)
plt.legend(loc=1)
plt.tight_layout()
plt.show()
#--------------------------------------------------

# Hledání "hits"

for i in range(scoreQ1.size):
    if scoreQ1[i] >= 0.9:
        print('hit Q1 = {}'.format(i), ', délka je: {}'.format(scoreQ1.size))
        print('čas: {}s'.format(t11[i]))#*16000))
        
        # "vyseknutí hit z původní nahrávky
        t1 = t11[i]*1000 # převedení na milisekundy
        t2 = t11[len(Q1_input)]*1000
        newAudio = AudioSegment.from_wav(inputFileS)
        newAudio = newAudio[t1:t2]
        newAudio.export('../hits/Q1_{}'.format(inputF), format="wav") #Exports to a wav file in the current path.
        break;
        
for i in range(scoreQ2.size):
    if scoreQ2[i] >= 0.9:
        print('hit Q2 = {}'.format(i),', délka je: {}'.format(scoreQ2.size))        
        print('čas: {}s'.format(t11[i]))#*16000))
        
        # "vyseknutí hit z původní nahrávky
        t1 = t11[i]*1000
        t2 = t11[len(Q2_input)]*1300
        newAudio = AudioSegment.from_wav(inputFileS)
        newAudio = newAudio[t1:t2]
        newAudio.export('../hits/Q2_{}'.format(inputF), format="wav") #Exports to a wav file in the current path.
        break;
    
    
    
    