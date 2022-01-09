# Gr23_Internet_Security

<h2>Tema: Komunikimi i sigurtë klient server</h2>
<br>

Grupi i projektit: <b>23</b> <br>Anëtarët: Festim BRAHA dhe Endrit SHAQIRI
<br>
Grupi i ushtrimeve: 2
<br>
<br>
Profesori: PHD.c Mërgim H. HOTI
<br>
<h2>Përshkrimi i punës së aplikacionit</h2>
Në këtë projekt janë përfshirë dy pjesë: Komunikimi i sigurtë mes serverit dhe klientëve duke përdorur RSA për konfidencialitetin dhe integritetin e të dhënave si dhe komunikimi mes serverit dhe klientëve me enkriptim të plotë për mesazhe(AES256) dhe Authentication(SHA256).
<br>


<h2>Komunikimi ndërmjet serverit dhe klientëve me enkriptim të plotë për mesazhe(AES256) dhe authentication(SHA256)</h2>
 Puna e aplikacionit:<br>
      * Shfaq klientët <br>
      * Dërgo mesazh te një klient specifik <br>
      * Dërgo mesazh për të gjithë klientët <br>
      * SHA256 për Authentication <br>
      * AES256 për mesazhe<br><br>
      
 Cka nevojitet:<br>
      * Python 3<br>
 
  Përdorimi:<br><br>
      * Fillimisht ekzekutohet serveri pastaj klienti<br>
      * Vendos HOST, PORT, Auth PASS, PASSPHRASE brenda programit të serverit.<br>
      * Vendos HOST-in e serverit, Portin brenda programit të klientit.
      * 
 
<h2>Aplikacioni me RSA</h2>
<h3>Procedurat e shkëmbimit të çelësave tek RSA:</h3>
1. Serveri hap një socket dhe klienti lidhet në atë socket.<br>
2. Klienti lexon dhe ruan çelësin publik të serverit nga file-i "serverPK.pem".<br>
3. Klienti zgjedh një string të rastësishëm si çelës sekret të mundshëm dhe e enkripton atë çelës duke përdorur çelësin publik të serverit.<br>
4. Klienti dërgon çelësin sekret të enkriptuar në server.<br>
5. Me marrjen e çelësit të enkriptuar, serveri dekripton mesazhin duke përdorur çelësin e tij privat.<br>
6. Serveri enkripton çelësin sekret me çelësin publik të klientit (i aksesueshëm për publikun) dhe dërgon mesazhin e enkriptuar te klienti.
7. Klienti dekripton mesazhin duke përdorur çelësin e tij privat dhe krahason plaintext-in me versionin e tij të çelësit sekret. Nëse janë të njëjta, procesi i vendosjes së çelësit është i suksesshëm. Përndryshe, përfundon lidhja.<br>
8. Diagram i thjeshte: Client: Enkriptimi(celesi sekret, celesi publik i serverit) Client  Server: Ciphertext Server: Dekriptimi(Ciphertext, Celesi privat i serverit) Server: Enkriptimi(Plaintext, celesi publik i klientit) Server  Client: Ciphertext Client: Dekriptimi(Ciphertext, celesi privat i klientit) If Plaintext != secret key: klienti përfundon(terminates) lidhjen.

<h3>Procedurat e komunikimit: Perspektiva e dërguesit(sender ose serverit)</h3>
1. Dërguesi gjeneron disa bajt të rastësishëm me gjatësi 12.<br>
2. Dërguesi krijon një cipher object duke përdorur çelësin e përbashkët sekret dhe random bytes. Cipher object është në modin CCM duke përdorur enkriptimin AES.<br>
3. Dërguesi enkripton ato random bytes duke përdorur cipher object dhe të dhënat e enkriptuara do të përdoren si IV(Initial Vector) random.<br>
4. Dërguesi krijon një cipher object tjeter duke përdorur IV-në e rastësishme dhe çelësin e përbashkët sekret. Cipher object është në modin CCM duke përdorur enkriptimin AES.<br>
5. Dërguesi enkripton mesazhin dhe gjeneron një etiketë(tag) (që përdoret për të siguruar integritetin e të dhënave) duke përdorur cipher objektin.<br>
6. Dërguesi dërgon IV të rastësishëm, mesazhin e enkriptuar dhe tag-un.<br>
7. Sa herë që synohet të dërgohet një mesazh, do të gjenerohet një IV e rastësishme (që do të thotë një cipher object i ri).<br>
8. Simple diagram: Random bytes = generate(12 bytes) Cipher = new AES(key=shared secret key, nonce=random bytes) Random IV = Cipher.encrypt(Random bytes) Another cipher2 = new AES(key=shared secret key, nonce=random IV) Ciphertext, tag = cipher2.encrypt_and_digest(plaintext) Message = ciphertext + b’@’ + random IV + b’@’ + tag Sender  Receiver: Message

<h3>Përspektiva e marrësit(klientit):</h3>
1. Marrësi nxjerr(extract) IV të rastësishme nga të dhënat e marra.<br>
2. Marrësi krijon një cipher object me IV te rastësishëm dhe çelësin e përbashkët(shared secret key). Cipher object përdor modin CCM me enkriptim AES.<br>
3. Marrësi dekripton dhe verifikon përmbajtjen dhe integritetin e të dhënave me cipher text-in dhe tagu-in.<br>
4. Nëse komprometohet integriteti, lidhja përfundon.<br>
5. Simple diagram: Ciphertext, random IV, tag = message.split(b’@’) Cipher = new AES(shared secret key, random IV) Plaintext = cipher.decrypt_and_verify(ciphertext, tag) If MAC check failed, receiver will terminate the connection

<br>
<h2>Referencat: https://www.youtube.com/watch?v=eSPBlI2PTyc</h2>







