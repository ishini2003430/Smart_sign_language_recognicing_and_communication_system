from . import lstm, gru, conv1d_bilstm
FACTORIES = {'lstm': lstm.build, 'gru': gru.build, 'conv1d_bilstm': conv1d_bilstm.build}
