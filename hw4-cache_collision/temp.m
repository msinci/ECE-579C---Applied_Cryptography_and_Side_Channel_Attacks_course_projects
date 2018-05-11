% Collision attack data analysis by MSI
clearvars -except timings;
clc;
load('ca_data.mat', 'timings')

% timings = zeros(10,500000,17);
% 
% for i=1:10
%     fname = strcat('ca_tada/ca_data',num2str(i));
%     timings(i,:,:) = textread(fname);
% end

bin = zeros(256,1);
cnt = zeros(256,1);
firstbyte = 11;
secondbyte = 12;

for i=1:10
   i
    for j=1:500000
    delta = bitxor(timings(i,j,firstbyte),timings(i,j,secondbyte));
        if timings(i,j,17)<400 % cut of for the outliers
            bin(delta+1) = bin(delta+1) + timings(i,j,17);
            cnt(delta+1) = cnt(delta+1) + 1;
        end 
    end
        
end

for index = 1:256
    bin(index) = bin(index)/cnt(index); % calculating the average for each state
end
plot(bin)  

% last round key for all zero input key is as follows
key = [hex2dec('b4'), hex2dec('ef'), hex2dec('5b'), hex2dec('cb'), hex2dec('3e'), hex2dec('92'), hex2dec('e2'), hex2dec('11'), hex2dec('23'), hex2dec('e9'), hex2dec('51'), hex2dec('cf'), hex2dec('6f'), hex2dec('8f'), hex2dec('18'), hex2dec('8e')];

delta = bitxor(key(firstbyte), key(secondbyte));

[val, pos] = min(bin);

if pos==delta+1
    display(['Correct delta is: ',num2str(delta)]);
else
%     temppos = pos+1;
    display([num2str(dec2hex(pos+1)),' is not the correct delta. maybe need more samples?']);
end
hold on
plot(delta+1,bin(delta+1),'+r')
hold off

