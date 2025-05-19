<?xml version="1.0" standalone="no"?>
<!DOCTYPE QML SYSTEM "QML_V3.dtd">

<QML>

<!-- SC - Scelta singola -->
<QUESTION ID="Q1" DESCRIPTION="Domanda SC" TOPIC="demo" STATUS="Normal">
  <CONTENT TYPE="text/html"><![CDATA[Qual è il colore del cielo in una giornata serena?]]></CONTENT>
  <ANSWER QTYPE="MC">
    <CHOICE ID="A1"><CONTENT TYPE="text/html"><![CDATA[Blu]]></CONTENT></CHOICE>
    <CHOICE ID="A2"><CONTENT TYPE="text/html"><![CDATA[Verde]]></CONTENT></CHOICE>
    <CHOICE ID="A3"><CONTENT TYPE="text/html"><![CDATA[Rosso]]></CONTENT></CHOICE>
  </ANSWER>
  <OUTCOME ID="O1" SCORE="1"><CONDITION>"A1"</CONDITION></OUTCOME>
</QUESTION>

<!-- MR - Risposte multiple -->
<QUESTION ID="Q2" DESCRIPTION="Domanda MR" TOPIC="demo" STATUS="Normal">
  <CONTENT TYPE="text/html"><![CDATA[Seleziona tutti i numeri pari:]]></CONTENT>
  <ANSWER QTYPE="MR">
    <CHOICE ID="B1"><CONTENT TYPE="text/html"><![CDATA[2]]></CONTENT></CHOICE>
    <CHOICE ID="B2"><CONTENT TYPE="text/html"><![CDATA[3]]></CONTENT></CHOICE>
    <CHOICE ID="B3"><CONTENT TYPE="text/html"><![CDATA[4]]></CONTENT></CHOICE>
  </ANSWER>
  <OUTCOME ID="MR1" SCORE="0.5"><CONDITION>"B1"</CONDITION></OUTCOME>
  <OUTCOME ID="MR2" SCORE="0.5"><CONDITION>"B3"</CONDITION></OUTCOME>
</QUESTION>

<!-- TF - Vero/Falso -->
<QUESTION ID="Q3" DESCRIPTION="Domanda TF" TOPIC="demo" STATUS="Normal">
  <CONTENT TYPE="text/html"><![CDATA[Il sole sorge ad ovest.]]></CONTENT>
  <ANSWER QTYPE="TF">
    <CHOICE ID="true"><CONTENT TYPE="text/html"><![CDATA[Vero]]></CONTENT></CHOICE>
    <CHOICE ID="false"><CONTENT TYPE="text/html"><![CDATA[Falso]]></CONTENT></CHOICE>
  </ANSWER>
  <OUTCOME ID="TF1" SCORE="1"><CONDITION>"false"</CONDITION></OUTCOME>
</QUESTION>

<!-- OPEN - Risposta aperta -->
<QUESTION ID="Q4" DESCRIPTION="Domanda OPEN" TOPIC="demo" STATUS="Normal">
  <CONTENT TYPE="text/html"><![CDATA[Qual è il nome del nostro pianeta?]]></CONTENT>
  <ANSWER QTYPE="OPEN">
    <CHOICE ID="OA1"><CONTENT TYPE="text/html"><![CDATA[Terra]]></CONTENT></CHOICE>
  </ANSWER>
  <OUTCOME ID="OOPEN1" SCORE="1"><CONDITION>"Terra"</CONDITION></OUTCOME>
</QUESTION>

<!-- NUM - Risposta numerica -->
<QUESTION ID="Q5" DESCRIPTION="Domanda NUM" TOPIC="demo" STATUS="Normal">
  <CONTENT TYPE="text/html"><![CDATA[Quanto fa 3 + 4?]]></CONTENT>
  <ANSWER QTYPE="NUM">
    <CHOICE ID="N1"><CONTENT TYPE="text/html"><![CDATA[7]]></CONTENT></CHOICE>
  </ANSWER>
  <OUTCOME ID="ONUM1" SCORE="1"><CONDITION>"7"</CONDITION></OUTCOME>
</QUESTION>

</QML>
