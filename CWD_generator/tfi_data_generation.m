clear
%% data dump
filename = 'FMCW_RADAR2022_dict_v_change.pkl';
fid=py.open(filename,'rb');
data=py.pickle.load(fid);

%% read data (type,snr)
% raw_key = py.list(keys(data));
% raw_key_cell = cell(raw_key);
% select = py.tuple({'T3',snrs(1)});
% value = double(data{select}.T);

% i,q to complex
% value_real = value(:,1,2);
% value_imag = value(:,2,2);
% value_complex = value_real + j*value_imag;
% sig = reshape(value_complex,[],10);

%% create folders
waveforms = {'LFM','Barker','Costas','Frank','P1','P2','P3','P4','T1','T2','T3','T4'};
datasetCWD = "dataset-CWD_various5";
fps = 100;
% filter configuration
g=kaiser(63,0.5);
h=kaiser(63,0.5);
imgSize = 224;

snrs = -20:2:10; % snr range
for i=1:length(waveforms)
    for ii=1:length(snrs)
        mkdir(fullfile(datasetCWD,waveforms{i},string(snrs(ii))))
    end 
end

%% CWD 

for n=1:length(snrs)
    disp(['SNR = ',sprintf('%+02d', snrs(n))])
    
    for k=1:length(waveforms)
        waveform = waveforms{k};
        switch waveform
            case 'LFM'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('LFM-snr%02d-no%05d.png',snrs(n),idx)));
                end
                
            case 'Barker'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('Barker-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'Costas'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('Costas-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'Frank'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('Frank-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'P1'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('P1-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'P2'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('P2-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'P3'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('P3-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'P4'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('P4-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'T1'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('T1-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'T2'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('T2-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'T3'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('T3-snr%02d-no%05d.png',snrs(n),idx)));
                end
            case 'T4'
                disp(['Generating ',waveform, ' waveform ...']);
                waveformfolderCWD = fullfile(datasetCWD,waveform,string(snrs(n)));
                for idx=1:fps
                    select = py.tuple({waveform,snrs(n)});
                    wav = double(data{select}.T);
                    % i,q to complex
                    wav_real = wav(:,1,idx);
                    wav_imag = wav(:,2,idx);
                    wav = wav_real + j*wav_imag;
                    t=1:length(wav);
                    [CWD_TFD,~,~] = FTCWD(wav,t,1024,g,h,1,0,imgSize);
                    imwrite(CWD_TFD,fullfile(waveformfolderCWD,sprintf('T4-snr%02d-no%05d.png',snrs(n),idx)));
                end
            otherwise
                disp('Done!')
        end
    end
end
        
                    
             

%% cwd
t_length = length(sig(1,:));
for k=1:1
%     origin_freq = fft(sig);
%     fft_shfit = fftshift(origin_freq);
%     half_IQ = ifft(origin_freq(len/2+1:end,:));
%     img_array = tfrcw(half_IQ);
    img_array = tfrcw(sig(:,k));
    img = imresize(img_array,0.5);
    subplot(1,1,k)
    
    imagesc(img)
    title('Test')
    
%     imshow(img_array)
end

%% plot figure for all snr ranges.
for k=1:length(waveforms)
    f = figure;
    set(f,'Position',[200,200,600,500])
    tx_type = waveforms(k);
    disp("tx type is"+" "+tx_type{1})
    for i=1:length(snrs)
        
      
        select = py.tuple({tx_type{1},snrs(i)});
        value = double(data{select}.T);
        % i,q to complex
        value_real = value(:,1,:);
        value_imag = value(:,2,:);
        value_complex = value_real + j*value_imag;
        sig = reshape(value_complex,[],100);

        img_array = tfrcw(sig(:,randi([0,9],1)));
        img = imresize(img_array,0.5);
        subplot(4,4,i)
        imagesc(img);
        

        title(tx_type{1}+" "+string(snrs(i))+'dB')
    %     imwrite(img, 'LFM.png','png');
    end
end