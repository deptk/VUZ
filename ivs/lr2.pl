% Отношение: duplicate_elements(+Source, -Target)

% Базовый случай: пустой список
duplicate_elements([], []).

% Рекурсивный случай: удвоение головы и обработка хвоста
duplicate_elements([H | T], [H, H | Rest]) :- duplicate_elements(T, Rest).
