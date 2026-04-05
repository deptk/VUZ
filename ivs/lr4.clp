;; ============================================
;; Экспертная система: Выбор система управления событиями безопасности (Security information and event management - SIEM)
;; Студент: Горчилин А.А.
;; Группа: ЭВМбз-22-1
;; ============================================

(deffunction ask-question (?question $?allowed-values)
   (printout t ?question)
   (bind ?answer (read))
   (if (lexemep ?answer) 
       then (bind ?answer (lowcase ?answer)))
   (while (not (member$ ?answer ?allowed-values)) do
      (printout t ?question)
      (bind ?answer (read))
      (if (lexemep ?answer) 
          then (bind ?answer (lowcase ?answer))))
   ?answer)

(deffunction yes-or-no-p (?question)
   (bind ?response (ask-question ?question yes no y n))
   (if (or (eq ?response yes) (eq ?response y))
       then TRUE 
       else FALSE))


;; ============================================
;; ПРАВИЛА ОПРЕДЕЛЕНИЯ БЮДЖЕТА
;; ============================================

(defrule ask-budget
   (not (budget ?))
   (not (recommend ?))
   =>
   (bind ?b (ask-question 
      "Какой у вас бюджет? (free/low/medium/high) [free=0, low<1m, medium=1-5m, high>5m]: "
      free low medium high))
   (assert (budget ?b)))

;; ============================================
;; ПРАВИЛА ОПРЕДЕЛЕНИЯ ЦЕЛЕЙ
;; ============================================
(defrule ask-platform
   (budget ?)
   (not (platform ?))
   (not (recommend ?))
   =>
   (if (yes-or-no-p "Вам нужна мультиплатформенная система? (yes/no): ")
       then (assert (platform yes))
       else (assert (planform no))))

(defrule ask-platform-type
   (platform no)
   (not (platform-type ?))
   (not (recommend ?))
   =>
   (bind ?ptype (ask-question 
      "Для какой платформы нужен SIEM? (linux/windows): "
      linux windows))
   (assert (platform-type ?ptype)))

(defrule ask-kb
   (budget ?)
   (not (kb ?))
   (not (recommend ?))
   =>
   (if (yes-or-no-p "Вам нужна возможность написания правил экспертизы событий? (yes/no): ")
       then (assert (kb yes))
       else (assert (kb no))))

(defrule ask-vm
   (budget ?)
   (not (vm ?))
   (not (recommend ?))
   =>
   (if (yes-or-no-p "Вам нужен модуль обнаружения и управления уязвимостями? (yes/no): ")
       then (assert (vm yes))
       else (assert (vm no))))

(defrule ask-hcc
   (budget ?)
   (not (hcc ?))
   (not (recommend ?))
   =>
   (if (yes-or-no-p "Вам нужен модуль для проверки соответствия стандартам кибербезопасности? (yes/no): ")
       then (assert (hcc yes))
       else (assert (hcc no))))

(defrule ask-fstek
   (budget ?)
   (not (fstek ?))
   (not (recommend ?))
   =>
   (if (yes-or-no-p "Вам нужно сертифицированное ФСТЭК решение? (yes/no): ")
       then (assert (fstek yes))
       else (assert (fstek no))))

;; ============================================
;; ПРАВИЛА РЕКОМЕНДАЦИЙ
;; ============================================

(defrule recommend-maxpatrol
   (budget high)
   (platform yes)
   (kb yes)
   (vm yes)
   (hcc yes)
   (fstek yes)
   (not (recommend ?))
   =>
   (assert (recommend "MaxPatrol SIEM")))

(defrule recommend-wazuh
   (budget free)
   (platform no)
   (platform-type linux)
   (kb no)
   (vm yes)
   (hcc yes)
   (fstek no)
   (not (recommend ?))
   =>
   (assert (recommend "Wazuh")))

(defrule recommend-elk
   (budget free)
   (platform yes)
   (or (platform-type linux) (platform-type windows))
   (kb yes)
   (vm no)
   (hcc no)
   (fstek no)
   (not (recommend ?))
   =>
   (assert (recommend "ELK / OpenSearch")))

(defrule recommend-kuma
   (budget medium)
   (platform no)
   (platform-type linux)
   (kb no)
   (vm no)
   (hcc no)
   (fstek yes)
   (not (recommend ?))
   =>
   (assert (recommend "Kaspersky KUMA")))

(defrule recommend-rusiem
   (budget low)
   (platform no)
   (platform-type linux)
   (kb no)
   (vm no)
   (hcc no)
   (fstek yes)
   (not (recommend ?))
   =>
   (assert (recommend "RuSIEM")))

(defrule recommend-solar
   (budget high)
   (platform yes)
   (kb yes)
   (vm no)
   (hcc no)
   (fstek no)
   (not (recommend ?))
   =>
   (assert (recommend "Solar SIEM")))

(defrule recommend-usergate
   (budget medium)
   (platform yes)
   (kb yes)
   (vm no)
   (hcc no)
   (fstek no)
   (not (recommend ?))
   =>
   (assert (recommend "UserGate SIEM")))

(defrule recommend-splunk
   (budget high)
   (platform yes)
   (kb yes)
   (vm yes)
   (hcc no)
   (fstek no)
   (not (recommend ?))
   =>
   (assert (recommend "Splunk")))

(defrule recommend-fallback
   (not (recommend ?))
   (budget ?b)
   =>
   (assert (recommend "Нет точного совпадения. Рассмотрите Wazuh (беспланая) или MaxPatrol (максимальные возможности)")))

;; ============================================
;; СТАРТОВЫЕ ПРАВИЛА
;; ============================================

(defrule start
   (initial-fact)
   =>
   (printout t crlf)
   (printout t "****************************************" crlf)
   (printout t "***   ПОДБОР SIEM - ЭКСПЕРТ   ***" crlf)
   (printout t "****************************************" crlf)
   (printout t crlf "Отвечайте на вопросы, я помогу выбрать SIEM." crlf crlf))

(defrule conclusion
   (recommend ?item)
   (not (already-printed))
   =>
   (printout t crlf "*** РЕКОМЕНДАЦИЯ: " ?item " ***" crlf crlf)
   (assert (already-printed)))
