# fun_with_JWTs
<p>
jku_tamper.py at the very least decodes the header and payload of a 
signed, not encrypted JWT.
</p>
<p>
if the jku key is present in the header, this gives the possibility of redirecting to a public key file we control.
</p>
<p>
this tool will create a JWT with edited jku and payload data, also creating a public key file to verify our signature.
</p>
