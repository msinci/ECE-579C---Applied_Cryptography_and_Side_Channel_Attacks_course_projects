%% Running the Attack
num_traces=500000;
pos0 = 11
pos1 = 12
bin = zeros(256,1);
cnt = zeros(256,1);

for fcount = 1:10
    fcount
    NAME = ['time',num2str(fcount),'_q2.txt'];
                ciphertext = textread(NAME);

    for trace = 1:num_traces
        delta = bitxor(ciphertext(trace,pos0),ciphertext(trace,pos1));
        if ciphertext(trace,17)<1000
            bin(delta+1) = bin(delta+1) + ciphertext(trace,17);
            cnt(delta+1) = cnt(delta+1) + 1;
        end
    end
end

for idx = 1:256
    bin(idx) = bin(idx)/cnt(idx);
end
plot(bin)

key = [hex2dec('b4'), hex2dec('ef'), hex2dec('5b'), hex2dec('cb'), hex2dec('3e'), hex2dec('92'), hex2dec('e2'), hex2dec('11'), hex2dec('23'), hex2dec('e9'), hex2dec('51'), hex2dec('cf'), hex2dec('6f'), hex2dec('8f'), hex2dec('18'), hex2dec('8e')];
delta = bitxor(key(pos0), key(pos1))
[val pos] = min(bin);
if pos==delta+1
    ['Correct key is: ',delta]
else
    ['hmpf']
end
hold on
plot(delta+1,bin(delta+1),'+r')
hold off
