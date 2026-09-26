
.\storage_serv:     file format elf64-x86-64


Disassembly of section .text:

0000000000e01920 <crosscall2@@Base+0x859800>:
  e01920:	49 3b 66 10          	cmp    rsp,QWORD PTR [r14+0x10]
  e01924:	76 52                	jbe    e01978 <crosscall2@@Base+0x859858>
  e01926:	55                   	push   rbp
  e01927:	48 89 e5             	mov    rbp,rsp
  e0192a:	48 83 ec 08          	sub    rsp,0x8
  e0192e:	4d 8b 66 20          	mov    r12,QWORD PTR [r14+0x20]
  e01932:	4d 85 e4             	test   r12,r12
  e01935:	0f 85 93 00 00 00    	jne    e019ce <crosscall2@@Base+0x8598ae>
  e0193b:	48 89 44 24 18       	mov    QWORD PTR [rsp+0x18],rax
  e01940:	48 89 5c 24 20       	mov    QWORD PTR [rsp+0x20],rbx
  e01945:	48 89 4c 24 28       	mov    QWORD PTR [rsp+0x28],rcx
  e0194a:	48 89 7c 24 30       	mov    QWORD PTR [rsp+0x30],rdi
  e0194f:	48 89 74 24 38       	mov    QWORD PTR [rsp+0x38],rsi
  e01954:	4c 89 44 24 40       	mov    QWORD PTR [rsp+0x40],r8
  e01959:	44 88 4c 24 48       	mov    BYTE PTR [rsp+0x48],r9b
  e0195e:	31 c0                	xor    eax,eax
  e01960:	e8 3b 34 67 ff       	call   474da0 <pam_start_confdir@plt+0x6f188>
  e01965:	48 8d 0d 94 ea 83 00 	lea    rcx,[rip+0x83ea94]        # 1640400 <cbPAMConv@@Base+0xd1250>
  e0196c:	48 89 c3             	mov    rbx,rax
  e0196f:	48 89 c8             	mov    rax,rcx
  e01972:	48 83 c4 08          	add    rsp,0x8
  e01976:	5d                   	pop    rbp
  e01977:	c3                   	ret
  e01978:	48 89 44 24 08       	mov    QWORD PTR [rsp+0x8],rax
  e0197d:	48 89 5c 24 10       	mov    QWORD PTR [rsp+0x10],rbx
  e01982:	48 89 4c 24 18       	mov    QWORD PTR [rsp+0x18],rcx
  e01987:	48 89 7c 24 20       	mov    QWORD PTR [rsp+0x20],rdi
  e0198c:	48 89 74 24 28       	mov    QWORD PTR [rsp+0x28],rsi
  e01991:	4c 89 44 24 30       	mov    QWORD PTR [rsp+0x30],r8
  e01996:	44 88 4c 24 38       	mov    BYTE PTR [rsp+0x38],r9b
  e0199b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
  e019a0:	e8 fb f8 67 ff       	call   4812a0 <pam_start_confdir@plt+0x7b688>
  e019a5:	48 8b 44 24 08       	mov    rax,QWORD PTR [rsp+0x8]
  e019aa:	48 8b 5c 24 10       	mov    rbx,QWORD PTR [rsp+0x10]
  e019af:	48 8b 4c 24 18       	mov    rcx,QWORD PTR [rsp+0x18]
  e019b4:	48 8b 7c 24 20       	mov    rdi,QWORD PTR [rsp+0x20]
  e019b9:	48 8b 74 24 28       	mov    rsi,QWORD PTR [rsp+0x28]
  e019be:	4c 8b 44 24 30       	mov    r8,QWORD PTR [rsp+0x30]
  e019c3:	44 0f b6 4c 24 38    	movzx  r9d,BYTE PTR [rsp+0x38]
  e019c9:	e9 52 ff ff ff       	jmp    e01920 <crosscall2@@Base+0x859800>
  e019ce:	4c 8d 6c 24 18       	lea    r13,[rsp+0x18]
  e019d3:	4d 39 2c 24          	cmp    QWORD PTR [r12],r13
  e019d7:	0f 85 5e ff ff ff    	jne    e0193b <crosscall2@@Base+0x85981b>
  e019dd:	49 89 24 24          	mov    QWORD PTR [r12],rsp
  e019e1:	e9 55 ff ff ff       	jmp    e0193b <crosscall2@@Base+0x85981b>
  e019e6:	cc                   	int3
  e019e7:	cc                   	int3
  e019e8:	cc                   	int3
  e019e9:	cc                   	int3
  e019ea:	cc                   	int3
  e019eb:	cc                   	int3
  e019ec:	cc                   	int3
  e019ed:	cc                   	int3
  e019ee:	cc                   	int3
  e019ef:	cc                   	int3
  e019f0:	cc                   	int3
  e019f1:	cc                   	int3
  e019f2:	cc                   	int3
  e019f3:	cc                   	int3
  e019f4:	cc                   	int3
  e019f5:	cc                   	int3
  e019f6:	cc                   	int3
  e019f7:	cc                   	int3
  e019f8:	cc                   	int3
  e019f9:	cc                   	int3
  e019fa:	cc                   	int3
  e019fb:	cc                   	int3
  e019fc:	cc                   	int3
  e019fd:	cc                   	int3
  e019fe:	cc                   	int3
  e019ff:	cc                   	int3
  e01a00:	49 3b 66 10          	cmp    rsp,QWORD PTR [r14+0x10]
  e01a04:	0f 86 9d 00 00 00    	jbe    e01aa7 <crosscall2@@Base+0x859987>
  e01a0a:	55                   	push   rbp
  e01a0b:	48 89 e5             	mov    rbp,rsp
  e01a0e:	48 83 ec 48          	sub    rsp,0x48
  e01a12:	4d 8b 66 20          	mov    r12,QWORD PTR [r14+0x20]
  e01a16:	4d 85 e4             	test   r12,r12
  e01a19:	0f 85 e6 00 00 00    	jne    e01b05 <crosscall2@@Base+0x8599e5>
  e01a1f:	48 89 44 24 58       	mov    QWORD PTR [rsp+0x58],rax
  e01a24:	48 89 5c 24 60       	mov    QWORD PTR [rsp+0x60],rbx
  e01a29:	48 89 4c 24 68       	mov    QWORD PTR [rsp+0x68],rcx
  e01a2e:	48 89 7c 24 70       	mov    QWORD PTR [rsp+0x70],rdi
  e01a33:	48 89 74 24 78       	mov    QWORD PTR [rsp+0x78],rsi
  e01a38:	4c 89 84 24 80 00 00 	mov    QWORD PTR [rsp+0x80],r8
  e01a3f:	00 
  e01a40:	44 88 8c 24 88 00 00 	mov    BYTE PTR [rsp+0x88],r9b
  e01a47:	00 
  e01a48:	48 8b 54 24 58       	mov    rdx,QWORD PTR [rsp+0x58]
  e01a4d:	48 89 54 24 10       	mov    QWORD PTR [rsp+0x10],rdx
  e01a52:	0f 10 44 24 60       	movups xmm0,XMMWORD PTR [rsp+0x60]
  e01a57:	0f 11 44 24 18       	movups XMMWORD PTR [rsp+0x18],xmm0
  e01a5c:	0f 10 44 24 70       	movups xmm0,XMMWORD PTR [rsp+0x70]
  e01a61:	0f 11 44 24 28       	movups XMMWORD PTR [rsp+0x28],xmm0
  e01a66:	0f 10 84 24 80 00 00 	movups xmm0,XMMWORD PTR [rsp+0x80]
  e01a6d:	00 
  e01a6e:	0f 11 44 24 38       	movups XMMWORD PTR [rsp+0x38],xmm0
  e01a73:	48 8b 4c 24 18       	mov    rcx,QWORD PTR [rsp+0x18]
  e01a78:	49 39 ca             	cmp    r10,rcx
  e01a7b:	73 21                	jae    e01a9e <crosscall2@@Base+0x85997e>
  e01a7d:	48 8b 4c 24 10       	mov    rcx,QWORD PTR [rsp+0x10]
  e01a82:	4a 8b 04 d1          	mov    rax,QWORD PTR [rcx+r10*8]
  e01a86:	e8 15 33 67 ff       	call   474da0 <pam_start_confdir@plt+0x6f188>
  e01a8b:	48 8d 0d 6e e9 83 00 	lea    rcx,[rip+0x83e96e]        # 1640400 <cbPAMConv@@Base+0xd1250>
  e01a92:	48 89 c3             	mov    rbx,rax
  e01a95:	48 89 c8             	mov    rax,rcx
  e01a98:	48 83 c4 48          	add    rsp,0x48
  e01a9c:	5d                   	pop    rbp
  e01a9d:	c3                   	ret
  e01a9e:	4c 89 d0             	mov    rax,r10
  e01aa1:	e8 9a 1a 68 ff       	call   483540 <_cgo_topofstack@@Base+0x420>
  e01aa6:	90                   	nop
  e01aa7:	48 89 44 24 08       	mov    QWORD PTR [rsp+0x8],rax
  e01aac:	48 89 5c 24 10       	mov    QWORD PTR [rsp+0x10],rbx
  e01ab1:	48 89 4c 24 18       	mov    QWORD PTR [rsp+0x18],rcx
  e01ab6:	48 89 7c 24 20       	mov    QWORD PTR [rsp+0x20],rdi
  e01abb:	48 89 74 24 28       	mov    QWORD PTR [rsp+0x28],rsi
  e01ac0:	4c 89 44 24 30       	mov    QWORD PTR [rsp+0x30],r8
  e01ac5:	44 88 4c 24 38       	mov    BYTE PTR [rsp+0x38],r9b
  e01aca:	4c 89 54 24 40       	mov    QWORD PTR [rsp+0x40],r10
  e01acf:	e8 cc f7 67 ff       	call   4812a0 <pam_start_confdir@plt+0x7b688>
  e01ad4:	48 8b 44 24 08       	mov    rax,QWORD PTR [rsp+0x8]
  e01ad9:	48 8b 5c 24 10       	mov    rbx,QWORD PTR [rsp+0x10]
  e01ade:	48 8b 4c 24 18       	mov    rcx,QWORD PTR [rsp+0x18]
  e01ae3:	48 8b 7c 24 20       	mov    rdi,QWORD PTR [rsp+0x20]
  e01ae8:	48 8b 74 24 28       	mov    rsi,QWORD PTR [rsp+0x28]
  e01aed:	4c 8b 44 24 30       	mov    r8,QWORD PTR [rsp+0x30]
  e01af2:	44 0f b6 4c 24 38    	movzx  r9d,BYTE PTR [rsp+0x38]
  e01af8:	4c 8b 54 24 40       	mov    r10,QWORD PTR [rsp+0x40]
  e01afd:	0f 1f 00             	nop    DWORD PTR [rax]
  e01b00:	e9 fb fe ff ff       	jmp    e01a00 <crosscall2@@Base+0x8598e0>
  e01b05:	4c 8d 6c 24 58       	lea    r13,[rsp+0x58]
  e01b0a:	4d 39 2c 24          	cmp    QWORD PTR [r12],r13
  e01b0e:	0f 85 0b ff ff ff    	jne    e01a1f <crosscall2@@Base+0x8598ff>
  e01b14:	49 89 24 24          	mov    QWORD PTR [r12],rsp
  e01b18:	e9 02 ff ff ff       	jmp    e01a1f <crosscall2@@Base+0x8598ff>
  e01b1d:	cc                   	int3
  e01b1e:	cc                   	int3
  e01b1f:	cc                   	int3
  e01b20:	55                   	push   rbp
  e01b21:	48 89 e5             	mov    rbp,rsp
  e01b24:	48 83 ec 38          	sub    rsp,0x38
  e01b28:	4d 8b 66 20          	mov    r12,QWORD PTR [r14+0x20]
  e01b2c:	4d 85 e4             	test   r12,r12
  e01b2f:	75 5f                	jne    e01b90 <crosscall2@@Base+0x859a70>
  e01b31:	48 89 44 24 48       	mov    QWORD PTR [rsp+0x48],rax
  e01b36:	48 89 5c 24 50       	mov    QWORD PTR [rsp+0x50],rbx
  e01b3b:	48 89 4c 24 58       	mov    QWORD PTR [rsp+0x58],rcx
  e01b40:	48 89 7c 24 60       	mov    QWORD PTR [rsp+0x60],rdi
  e01b45:	48 89 74 24 68       	mov    QWORD PTR [rsp+0x68],rsi
  e01b4a:	4c 89 44 24 70       	mov    QWORD PTR [rsp+0x70],r8
  e01b4f:	44 88 4c 24 78       	mov    BYTE PTR [rsp+0x78],r9b
  e01b54:	48 8b 54 24 48       	mov    rdx,QWORD PTR [rsp+0x48]
  e01b59:	48 89 14 24          	mov    QWORD PTR [rsp],rdx
  e01b5d:	0f 10 44 24 50       	movups xmm0,XMMWORD PTR [rsp+0x50]
  e01b62:	0f 11 44 24 08       	movups XMMWORD PTR [rsp+0x8],xmm0
  e01b67:	0f 10 44 24 60       	movups xmm0,XMMWORD PTR [rsp+0x60]
  e01b6c:	0f 11 44 24 18       	movups XMMWORD PTR [rsp+0x18],xmm0
  e01b71:	0f 10 44 24 70       	movups xmm0,XMMWORD PTR [rsp+0x70]
  e01b76:	0f 11 44 24 28       	movups XMMWORD PTR [rsp+0x28],xmm0
  e01b7b:	48 8b 44 24 18       	mov    rax,QWORD PTR [rsp+0x18]
  e01b80:	48 8b 5c 24 20       	mov    rbx,QWORD PTR [rsp+0x20]
  e01b85:	48 8b 4c 24 28       	mov    rcx,QWORD PTR [rsp+0x28]
  e01b8a:	48 83 c4 38          	add    rsp,0x38
  e01b8e:	5d                   	pop    rbp
  e01b8f:	c3                   	ret
  e01b90:	4c 8d 6c 24 48       	lea    r13,[rsp+0x48]
  e01b95:	4d 39 2c 24          	cmp    QWORD PTR [r12],r13
  e01b99:	75 96                	jne    e01b31 <crosscall2@@Base+0x859a11>
  e01b9b:	49 89 24 24          	mov    QWORD PTR [r12],rsp
  e01b9f:	90                   	nop
  e01ba0:	eb 8f                	jmp    e01b31 <crosscall2@@Base+0x859a11>
  e01ba2:	cc                   	int3
  e01ba3:	cc                   	int3
  e01ba4:	cc                   	int3
  e01ba5:	cc                   	int3
  e01ba6:	cc                   	int3
  e01ba7:	cc                   	int3
  e01ba8:	cc                   	int3
  e01ba9:	cc                   	int3
  e01baa:	cc                   	int3
  e01bab:	cc                   	int3
  e01bac:	cc                   	int3
  e01bad:	cc                   	int3
  e01bae:	cc                   	int3
  e01baf:	cc                   	int3
  e01bb0:	cc                   	int3
  e01bb1:	cc                   	int3
  e01bb2:	cc                   	int3
  e01bb3:	cc                   	int3
  e01bb4:	cc                   	int3
  e01bb5:	cc                   	int3
  e01bb6:	cc                   	int3
  e01bb7:	cc                   	int3
  e01bb8:	cc                   	int3
  e01bb9:	cc                   	int3
  e01bba:	cc                   	int3
  e01bbb:	cc                   	int3
  e01bbc:	cc                   	int3
  e01bbd:	cc                   	int3
  e01bbe:	cc                   	int3
  e01bbf:	cc                   	int3
  e01bc0:	4c 8d a4 24 a0 fd ff 	lea    r12,[rsp-0x260]
  e01bc7:	ff 
  e01bc8:	4d 3b 66 10          	cmp    r12,QWORD PTR [r14+0x10]
  e01bcc:	0f 86 88 0e 00 00    	jbe    e02a5a <crosscall2@@Base+0x85a93a>
  e01bd2:	55                   	push   rbp
  e01bd3:	48 89 e5             	mov    rbp,rsp
  e01bd6:	48 81 ec d8 02 00 00 	sub    rsp,0x2d8
  e01bdd:	48 89 84 24 e8 02 00 	mov    QWORD PTR [rsp+0x2e8],rax
  e01be4:	00 
  e01be5:	48 89 9c 24 f0 02 00 	mov    QWORD PTR [rsp+0x2f0],rbx
  e01bec:	00 
  e01bed:	48 89 bc 24 00 03 00 	mov    QWORD PTR [rsp+0x300],rdi
  e01bf4:	00 
  e01bf5:	48 89 8c 24 f8 02 00 	mov    QWORD PTR [rsp+0x2f8],rcx
  e01bfc:	00 
  e01bfd:	48 89 fe             	mov    rsi,rdi
  e01c00:	48 89 cf             	mov    rdi,rcx
  e01c03:	b9 01 00 00 00       	mov    ecx,0x1
  e01c08:	31 c0                	xor    eax,eax
  e01c0a:	48 8d 1d a7 e2 d4 00 	lea    rbx,[rip+0xd4e2a7]        # 1b4feb8 <cbPAMConv@@Base+0x5e0d08>
  e01c11:	e8 4a ce 65 ff       	call   45ea60 <pam_start_confdir@plt+0x58e48>
  e01c16:	48 89 84 24 10 01 00 	mov    QWORD PTR [rsp+0x110],rax
  e01c1d:	00 
  e01c1e:	48 89 5c 24 30       	mov    QWORD PTR [rsp+0x30],rbx
  e01c23:	48 c7 44 24 28 00 00 	mov    QWORD PTR [rsp+0x28],0x0
  e01c2a:	00 00 
  e01c2c:	48 c7 44 24 38 00 00 	mov    QWORD PTR [rsp+0x38],0x0
  e01c33:	00 00 
  e01c35:	48 8b 94 24 e8 02 00 	mov    rdx,QWORD PTR [rsp+0x2e8]
  e01c3c:	00 
  e01c3d:	4c 8b 02             	mov    r8,QWORD PTR [rdx]
  e01c40:	4c 89 84 24 e8 01 00 	mov    QWORD PTR [rsp+0x1e8],r8
  e01c47:	00 
  e01c48:	4c 8d 44 24 38       	lea    r8,[rsp+0x38]
  e01c4d:	4c 89 84 24 f0 01 00 	mov    QWORD PTR [rsp+0x1f0],r8
  e01c54:	00 
  e01c55:	4c 8b 84 24 e8 01 00 	mov    r8,QWORD PTR [rsp+0x1e8]
  e01c5c:	00 
  e01c5d:	0f 1f 00             	nop    DWORD PTR [rax]
  e01c60:	4d 85 c0             	test   r8,r8
  e01c63:	74 09                	je     e01c6e <crosscall2@@Base+0x859b4e>
  e01c65:	48 8d 0d 6c 5b d8 00 	lea    rcx,[rip+0xd85b6c]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e01c6c:	eb 05                	jmp    e01c73 <crosscall2@@Base+0x859b53>
  e01c6e:	31 c9                	xor    ecx,ecx
  e01c70:	45 31 c0             	xor    r8d,r8d
  e01c73:	48 89 8c 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rcx
  e01c7a:	00 
  e01c7b:	4c 89 84 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],r8
  e01c82:	00 
  e01c83:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e01c8a:	00 
  e01c8b:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e01c8f:	48 8d 05 6a 5d 8d 00 	lea    rax,[rip+0x8d5d6a]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e01c96:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e01c9d:	00 
  e01c9e:	66 90                	xchg   ax,ax
  e01ca0:	e8 5b 44 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e01ca5:	48 8b 94 24 00 03 00 	mov    rdx,QWORD PTR [rsp+0x300]
  e01cac:	00 
  e01cad:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e01cb1:	83 3d f8 7e af 01 00 	cmp    DWORD PTR [rip+0x1af7ef8],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e01cb8:	75 12                	jne    e01ccc <crosscall2@@Base+0x859bac>
  e01cba:	48 8b 8c 24 f8 02 00 	mov    rcx,QWORD PTR [rsp+0x2f8]
  e01cc1:	00 
  e01cc2:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e01cc9:	00 
  e01cca:	eb 27                	jmp    e01cf3 <crosscall2@@Base+0x859bd3>
  e01ccc:	e8 ef 14 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e01cd1:	48 8b 8c 24 f8 02 00 	mov    rcx,QWORD PTR [rsp+0x2f8]
  e01cd8:	00 
  e01cd9:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e01cdc:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e01cdf:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e01ce3:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e01cea:	00 
  e01ceb:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e01cef:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e01cf3:	48 89 08             	mov    QWORD PTR [rax],rcx
  e01cf6:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e01cfd:	00 
  e01cfe:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e01d02:	48 8d 05 17 5e 8d 00 	lea    rax,[rip+0x8d5e17]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e01d09:	e8 12 54 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e01d0e:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e01d15:	00 
  e01d16:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e01d1a:	48 8d 05 1f 5f 8d 00 	lea    rax,[rip+0x8d5f1f]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e01d21:	e8 fa 53 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e01d26:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e01d2d:	00 
  e01d2e:	48 8b 51 08          	mov    rdx,QWORD PTR [rcx+0x8]
  e01d32:	48 89 94 24 d8 01 00 	mov    QWORD PTR [rsp+0x1d8],rdx
  e01d39:	00 
  e01d3a:	48 8d 54 24 28       	lea    rdx,[rsp+0x28]
  e01d3f:	48 89 94 24 e0 01 00 	mov    QWORD PTR [rsp+0x1e0],rdx
  e01d46:	00 
  e01d47:	48 8b 94 24 d8 01 00 	mov    rdx,QWORD PTR [rsp+0x1d8]
  e01d4e:	00 
  e01d4f:	48 85 d2             	test   rdx,rdx
  e01d52:	74 09                	je     e01d5d <crosscall2@@Base+0x859c3d>
  e01d54:	48 8d 05 7d 5a d8 00 	lea    rax,[rip+0xd85a7d]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e01d5b:	eb 04                	jmp    e01d61 <crosscall2@@Base+0x859c41>
  e01d5d:	31 c0                	xor    eax,eax
  e01d5f:	31 d2                	xor    edx,edx
  e01d61:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e01d68:	00 
  e01d69:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e01d70:	00 
  e01d71:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e01d78:	00 
  e01d79:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e01d7d:	48 8d 05 7c 5c 8d 00 	lea    rax,[rip+0x8d5c7c]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e01d84:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e01d8b:	00 
  e01d8c:	e8 6f 43 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e01d91:	48 8b 94 24 00 03 00 	mov    rdx,QWORD PTR [rsp+0x300]
  e01d98:	00 
  e01d99:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e01d9d:	83 3d 0c 7e af 01 00 	cmp    DWORD PTR [rip+0x1af7e0c],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e01da4:	75 12                	jne    e01db8 <crosscall2@@Base+0x859c98>
  e01da6:	48 8b 8c 24 f8 02 00 	mov    rcx,QWORD PTR [rsp+0x2f8]
  e01dad:	00 
  e01dae:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e01db5:	00 
  e01db6:	eb 27                	jmp    e01ddf <crosscall2@@Base+0x859cbf>
  e01db8:	e8 03 14 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e01dbd:	48 8b 8c 24 f8 02 00 	mov    rcx,QWORD PTR [rsp+0x2f8]
  e01dc4:	00 
  e01dc5:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e01dc8:	48 8b 10             	mov    rdx,QWORD PTR [rax]
  e01dcb:	49 89 53 08          	mov    QWORD PTR [r11+0x8],rdx
  e01dcf:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e01dd6:	00 
  e01dd7:	48 8b 72 20          	mov    rsi,QWORD PTR [rdx+0x20]
  e01ddb:	49 89 73 10          	mov    QWORD PTR [r11+0x10],rsi
  e01ddf:	48 89 08             	mov    QWORD PTR [rax],rcx
  e01de2:	48 c7 42 20 00 00 00 	mov    QWORD PTR [rdx+0x20],0x0
  e01de9:	00 
  e01dea:	48 8b 5a 28          	mov    rbx,QWORD PTR [rdx+0x28]
  e01dee:	48 8d 05 2b 5d 8d 00 	lea    rax,[rip+0x8d5d2b]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e01df5:	e8 26 53 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e01dfa:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e01e01:	00 
  e01e02:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e01e06:	48 8d 05 33 5e 8d 00 	lea    rax,[rip+0x8d5e33]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e01e0d:	e8 0e 53 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e01e12:	44 0f 11 7c 24 40    	movups XMMWORD PTR [rsp+0x40],xmm15
  e01e18:	48 c7 44 24 50 00 00 	mov    QWORD PTR [rsp+0x50],0x0
  e01e1f:	00 00 
  e01e21:	44 0f 11 bc 24 b0 02 	movups XMMWORD PTR [rsp+0x2b0],xmm15
  e01e28:	00 00 
  e01e2a:	48 c7 84 24 c0 02 00 	mov    QWORD PTR [rsp+0x2c0],0x0
  e01e31:	00 00 00 00 00 
  e01e36:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e01e3d:	00 
  e01e3e:	48 8b 51 10          	mov    rdx,QWORD PTR [rcx+0x10]
  e01e42:	48 89 94 24 c8 01 00 	mov    QWORD PTR [rsp+0x1c8],rdx
  e01e49:	00 
  e01e4a:	48 8d 94 24 b0 02 00 	lea    rdx,[rsp+0x2b0]
  e01e51:	00 
  e01e52:	48 89 94 24 d0 01 00 	mov    QWORD PTR [rsp+0x1d0],rdx
  e01e59:	00 
  e01e5a:	48 8b 94 24 c8 01 00 	mov    rdx,QWORD PTR [rsp+0x1c8]
  e01e61:	00 
  e01e62:	48 85 d2             	test   rdx,rdx
  e01e65:	74 09                	je     e01e70 <crosscall2@@Base+0x859d50>
  e01e67:	48 8d 05 6a 59 d8 00 	lea    rax,[rip+0xd8596a]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e01e6e:	eb 04                	jmp    e01e74 <crosscall2@@Base+0x859d54>
  e01e70:	31 c0                	xor    eax,eax
  e01e72:	31 d2                	xor    edx,edx
  e01e74:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e01e7b:	00 
  e01e7c:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e01e83:	00 
  e01e84:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e01e8b:	00 
  e01e8c:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e01e90:	48 8d 05 69 5b 8d 00 	lea    rax,[rip+0x8d5b69]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e01e97:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e01e9e:	00 
  e01e9f:	90                   	nop
  e01ea0:	e8 5b 42 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e01ea5:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e01eaa:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e01eae:	83 3d fb 7c af 01 00 	cmp    DWORD PTR [rip+0x1af7cfb],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e01eb5:	75 12                	jne    e01ec9 <crosscall2@@Base+0x859da9>
  e01eb7:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e01ebe:	00 
  e01ebf:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e01ec6:	00 
  e01ec7:	eb 27                	jmp    e01ef0 <crosscall2@@Base+0x859dd0>
  e01ec9:	e8 f2 12 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e01ece:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e01ed5:	00 
  e01ed6:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e01ed9:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e01edc:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e01ee0:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e01ee7:	00 
  e01ee8:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e01eec:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e01ef0:	48 89 08             	mov    QWORD PTR [rax],rcx
  e01ef3:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e01efa:	00 
  e01efb:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e01eff:	48 8d 05 1a 5c 8d 00 	lea    rax,[rip+0x8d5c1a]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e01f06:	e8 15 52 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e01f0b:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e01f12:	00 
  e01f13:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e01f17:	48 8d 05 22 5d 8d 00 	lea    rax,[rip+0x8d5d22]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e01f1e:	66 90                	xchg   ax,ax
  e01f20:	e8 fb 51 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e01f25:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e01f2c:	00 
  e01f2d:	48 8b 51 18          	mov    rdx,QWORD PTR [rcx+0x18]
  e01f31:	48 89 94 24 b8 01 00 	mov    QWORD PTR [rsp+0x1b8],rdx
  e01f38:	00 
  e01f39:	48 8d 54 24 40       	lea    rdx,[rsp+0x40]
  e01f3e:	48 89 94 24 c0 01 00 	mov    QWORD PTR [rsp+0x1c0],rdx
  e01f45:	00 
  e01f46:	48 8b 94 24 b8 01 00 	mov    rdx,QWORD PTR [rsp+0x1b8]
  e01f4d:	00 
  e01f4e:	48 85 d2             	test   rdx,rdx
  e01f51:	74 09                	je     e01f5c <crosscall2@@Base+0x859e3c>
  e01f53:	48 8d 05 7e 58 d8 00 	lea    rax,[rip+0xd8587e]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e01f5a:	eb 04                	jmp    e01f60 <crosscall2@@Base+0x859e40>
  e01f5c:	31 c0                	xor    eax,eax
  e01f5e:	31 d2                	xor    edx,edx
  e01f60:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e01f67:	00 
  e01f68:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e01f6f:	00 
  e01f70:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e01f77:	00 
  e01f78:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e01f7c:	48 8d 05 7d 5a 8d 00 	lea    rax,[rip+0x8d5a7d]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e01f83:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e01f8a:	00 
  e01f8b:	e8 70 41 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e01f90:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e01f95:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e01f99:	83 3d 10 7c af 01 00 	cmp    DWORD PTR [rip+0x1af7c10],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e01fa0:	75 12                	jne    e01fb4 <crosscall2@@Base+0x859e94>
  e01fa2:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e01fa9:	00 
  e01faa:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e01fb1:	00 
  e01fb2:	eb 27                	jmp    e01fdb <crosscall2@@Base+0x859ebb>
  e01fb4:	e8 07 12 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e01fb9:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e01fc0:	00 
  e01fc1:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e01fc4:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e01fc7:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e01fcb:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e01fd2:	00 
  e01fd3:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e01fd7:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e01fdb:	48 89 08             	mov    QWORD PTR [rax],rcx
  e01fde:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e01fe5:	00 
  e01fe6:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e01fea:	48 8d 05 2f 5b 8d 00 	lea    rax,[rip+0x8d5b2f]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e01ff1:	e8 2a 51 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e01ff6:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e01ffd:	00 
  e01ffe:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02002:	48 8d 05 37 5c 8d 00 	lea    rax,[rip+0x8d5c37]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e02009:	e8 12 51 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e0200e:	44 0f 11 7c 24 58    	movups XMMWORD PTR [rsp+0x58],xmm15
  e02014:	48 c7 44 24 68 00 00 	mov    QWORD PTR [rsp+0x68],0x0
  e0201b:	00 00 
  e0201d:	44 0f 11 bc 24 98 02 	movups XMMWORD PTR [rsp+0x298],xmm15
  e02024:	00 00 
  e02026:	48 c7 84 24 a8 02 00 	mov    QWORD PTR [rsp+0x2a8],0x0
  e0202d:	00 00 00 00 00 
  e02032:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e02039:	00 
  e0203a:	48 8b 51 20          	mov    rdx,QWORD PTR [rcx+0x20]
  e0203e:	48 89 94 24 a8 01 00 	mov    QWORD PTR [rsp+0x1a8],rdx
  e02045:	00 
  e02046:	48 8d 94 24 98 02 00 	lea    rdx,[rsp+0x298]
  e0204d:	00 
  e0204e:	48 89 94 24 b0 01 00 	mov    QWORD PTR [rsp+0x1b0],rdx
  e02055:	00 
  e02056:	48 8b 94 24 a8 01 00 	mov    rdx,QWORD PTR [rsp+0x1a8]
  e0205d:	00 
  e0205e:	66 90                	xchg   ax,ax
  e02060:	48 85 d2             	test   rdx,rdx
  e02063:	74 09                	je     e0206e <crosscall2@@Base+0x859f4e>
  e02065:	48 8d 05 6c 57 d8 00 	lea    rax,[rip+0xd8576c]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e0206c:	eb 04                	jmp    e02072 <crosscall2@@Base+0x859f52>
  e0206e:	31 c0                	xor    eax,eax
  e02070:	31 d2                	xor    edx,edx
  e02072:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e02079:	00 
  e0207a:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e02081:	00 
  e02082:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e02089:	00 
  e0208a:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e0208e:	48 8d 05 6b 59 8d 00 	lea    rax,[rip+0x8d596b]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e02095:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e0209c:	00 
  e0209d:	0f 1f 00             	nop    DWORD PTR [rax]
  e020a0:	e8 5b 40 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e020a5:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e020aa:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e020ae:	83 3d fb 7a af 01 00 	cmp    DWORD PTR [rip+0x1af7afb],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e020b5:	75 12                	jne    e020c9 <crosscall2@@Base+0x859fa9>
  e020b7:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e020be:	00 
  e020bf:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e020c6:	00 
  e020c7:	eb 27                	jmp    e020f0 <crosscall2@@Base+0x859fd0>
  e020c9:	e8 f2 10 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e020ce:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e020d5:	00 
  e020d6:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e020d9:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e020dc:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e020e0:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e020e7:	00 
  e020e8:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e020ec:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e020f0:	48 89 08             	mov    QWORD PTR [rax],rcx
  e020f3:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e020fa:	00 
  e020fb:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e020ff:	48 8d 05 1a 5a 8d 00 	lea    rax,[rip+0x8d5a1a]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e02106:	e8 15 50 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e0210b:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e02112:	00 
  e02113:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02117:	48 8d 05 22 5b 8d 00 	lea    rax,[rip+0x8d5b22]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e0211e:	66 90                	xchg   ax,ax
  e02120:	e8 fb 4f 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02125:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e0212c:	00 
  e0212d:	48 8b 51 28          	mov    rdx,QWORD PTR [rcx+0x28]
  e02131:	48 89 94 24 98 01 00 	mov    QWORD PTR [rsp+0x198],rdx
  e02138:	00 
  e02139:	48 8d 54 24 58       	lea    rdx,[rsp+0x58]
  e0213e:	48 89 94 24 a0 01 00 	mov    QWORD PTR [rsp+0x1a0],rdx
  e02145:	00 
  e02146:	48 8b 94 24 98 01 00 	mov    rdx,QWORD PTR [rsp+0x198]
  e0214d:	00 
  e0214e:	48 85 d2             	test   rdx,rdx
  e02151:	74 09                	je     e0215c <crosscall2@@Base+0x85a03c>
  e02153:	48 8d 05 7e 56 d8 00 	lea    rax,[rip+0xd8567e]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e0215a:	eb 04                	jmp    e02160 <crosscall2@@Base+0x85a040>
  e0215c:	31 c0                	xor    eax,eax
  e0215e:	31 d2                	xor    edx,edx
  e02160:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e02167:	00 
  e02168:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e0216f:	00 
  e02170:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e02177:	00 
  e02178:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e0217c:	48 8d 05 7d 58 8d 00 	lea    rax,[rip+0x8d587d]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e02183:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e0218a:	00 
  e0218b:	e8 70 3f 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e02190:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e02195:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e02199:	83 3d 10 7a af 01 00 	cmp    DWORD PTR [rip+0x1af7a10],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e021a0:	75 12                	jne    e021b4 <crosscall2@@Base+0x85a094>
  e021a2:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e021a9:	00 
  e021aa:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e021b1:	00 
  e021b2:	eb 27                	jmp    e021db <crosscall2@@Base+0x85a0bb>
  e021b4:	e8 07 10 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e021b9:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e021c0:	00 
  e021c1:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e021c4:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e021c7:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e021cb:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e021d2:	00 
  e021d3:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e021d7:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e021db:	48 89 08             	mov    QWORD PTR [rax],rcx
  e021de:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e021e5:	00 
  e021e6:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e021ea:	48 8d 05 2f 59 8d 00 	lea    rax,[rip+0x8d592f]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e021f1:	e8 2a 4f 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e021f6:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e021fd:	00 
  e021fe:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02202:	48 8d 05 37 5a 8d 00 	lea    rax,[rip+0x8d5a37]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e02209:	e8 12 4f 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e0220e:	44 0f 11 bc 24 a0 00 	movups XMMWORD PTR [rsp+0xa0],xmm15
  e02215:	00 00 
  e02217:	44 0f 11 bc 24 a8 00 	movups XMMWORD PTR [rsp+0xa8],xmm15
  e0221e:	00 00 
  e02220:	44 0f 11 bc 24 b8 00 	movups XMMWORD PTR [rsp+0xb8],xmm15
  e02227:	00 00 
  e02229:	44 0f 11 bc 24 c8 00 	movups XMMWORD PTR [rsp+0xc8],xmm15
  e02230:	00 00 
  e02232:	44 0f 11 bc 24 60 02 	movups XMMWORD PTR [rsp+0x260],xmm15
  e02239:	00 00 
  e0223b:	44 0f 11 bc 24 68 02 	movups XMMWORD PTR [rsp+0x268],xmm15
  e02242:	00 00 
  e02244:	44 0f 11 bc 24 78 02 	movups XMMWORD PTR [rsp+0x278],xmm15
  e0224b:	00 00 
  e0224d:	44 0f 11 bc 24 88 02 	movups XMMWORD PTR [rsp+0x288],xmm15
  e02254:	00 00 
  e02256:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e0225d:	00 
  e0225e:	48 8b 51 30          	mov    rdx,QWORD PTR [rcx+0x30]
  e02262:	48 89 94 24 88 01 00 	mov    QWORD PTR [rsp+0x188],rdx
  e02269:	00 
  e0226a:	48 8d 94 24 60 02 00 	lea    rdx,[rsp+0x260]
  e02271:	00 
  e02272:	48 89 94 24 90 01 00 	mov    QWORD PTR [rsp+0x190],rdx
  e02279:	00 
  e0227a:	48 8b 94 24 88 01 00 	mov    rdx,QWORD PTR [rsp+0x188]
  e02281:	00 
  e02282:	48 85 d2             	test   rdx,rdx
  e02285:	74 09                	je     e02290 <crosscall2@@Base+0x85a170>
  e02287:	48 8d 05 4a 55 d8 00 	lea    rax,[rip+0xd8554a]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e0228e:	eb 04                	jmp    e02294 <crosscall2@@Base+0x85a174>
  e02290:	31 c0                	xor    eax,eax
  e02292:	31 d2                	xor    edx,edx
  e02294:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e0229b:	00 
  e0229c:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e022a3:	00 
  e022a4:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e022ab:	00 
  e022ac:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e022b0:	48 8d 05 49 57 8d 00 	lea    rax,[rip+0x8d5749]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e022b7:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e022be:	00 
  e022bf:	90                   	nop
  e022c0:	e8 3b 3e 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e022c5:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e022ca:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e022ce:	83 3d db 78 af 01 00 	cmp    DWORD PTR [rip+0x1af78db],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e022d5:	75 12                	jne    e022e9 <crosscall2@@Base+0x85a1c9>
  e022d7:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e022de:	00 
  e022df:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e022e6:	00 
  e022e7:	eb 27                	jmp    e02310 <crosscall2@@Base+0x85a1f0>
  e022e9:	e8 d2 0e 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e022ee:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e022f5:	00 
  e022f6:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e022f9:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e022fc:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e02300:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e02307:	00 
  e02308:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e0230c:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e02310:	48 89 08             	mov    QWORD PTR [rax],rcx
  e02313:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e0231a:	00 
  e0231b:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e0231f:	48 8d 05 fa 57 8d 00 	lea    rax,[rip+0x8d57fa]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e02326:	e8 f5 4d 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e0232b:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e02332:	00 
  e02333:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02337:	48 8d 05 02 59 8d 00 	lea    rax,[rip+0x8d5902]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e0233e:	66 90                	xchg   ax,ax
  e02340:	e8 db 4d 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02345:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e0234c:	00 
  e0234d:	48 8b 51 38          	mov    rdx,QWORD PTR [rcx+0x38]
  e02351:	48 89 94 24 78 01 00 	mov    QWORD PTR [rsp+0x178],rdx
  e02358:	00 
  e02359:	48 8d 94 24 a0 00 00 	lea    rdx,[rsp+0xa0]
  e02360:	00 
  e02361:	48 89 94 24 80 01 00 	mov    QWORD PTR [rsp+0x180],rdx
  e02368:	00 
  e02369:	48 8b 94 24 78 01 00 	mov    rdx,QWORD PTR [rsp+0x178]
  e02370:	00 
  e02371:	48 85 d2             	test   rdx,rdx
  e02374:	74 09                	je     e0237f <crosscall2@@Base+0x85a25f>
  e02376:	48 8d 05 5b 54 d8 00 	lea    rax,[rip+0xd8545b]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e0237d:	eb 04                	jmp    e02383 <crosscall2@@Base+0x85a263>
  e0237f:	31 c0                	xor    eax,eax
  e02381:	31 d2                	xor    edx,edx
  e02383:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e0238a:	00 
  e0238b:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e02392:	00 
  e02393:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e0239a:	00 
  e0239b:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e0239f:	48 8d 05 5a 56 8d 00 	lea    rax,[rip+0x8d565a]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e023a6:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e023ad:	00 
  e023ae:	e8 4d 3d 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e023b3:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e023b8:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e023bc:	83 3d ed 77 af 01 00 	cmp    DWORD PTR [rip+0x1af77ed],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e023c3:	75 12                	jne    e023d7 <crosscall2@@Base+0x85a2b7>
  e023c5:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e023cc:	00 
  e023cd:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e023d4:	00 
  e023d5:	eb 27                	jmp    e023fe <crosscall2@@Base+0x85a2de>
  e023d7:	e8 e4 0d 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e023dc:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e023e3:	00 
  e023e4:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e023e7:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e023ea:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e023ee:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e023f5:	00 
  e023f6:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e023fa:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e023fe:	48 89 08             	mov    QWORD PTR [rax],rcx
  e02401:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e02408:	00 
  e02409:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e0240d:	48 8d 05 0c 57 8d 00 	lea    rax,[rip+0x8d570c]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e02414:	e8 07 4d 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02419:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e02420:	00 
  e02421:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02425:	48 8d 05 14 58 8d 00 	lea    rax,[rip+0x8d5814]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e0242c:	e8 ef 4c 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02431:	44 0f 11 bc 24 d8 00 	movups XMMWORD PTR [rsp+0xd8],xmm15
  e02438:	00 00 
  e0243a:	44 0f 11 bc 24 e0 00 	movups XMMWORD PTR [rsp+0xe0],xmm15
  e02441:	00 00 
  e02443:	44 0f 11 bc 24 f0 00 	movups XMMWORD PTR [rsp+0xf0],xmm15
  e0244a:	00 00 
  e0244c:	44 0f 11 bc 24 00 01 	movups XMMWORD PTR [rsp+0x100],xmm15
  e02453:	00 00 
  e02455:	44 0f 11 bc 24 28 02 	movups XMMWORD PTR [rsp+0x228],xmm15
  e0245c:	00 00 
  e0245e:	44 0f 11 bc 24 30 02 	movups XMMWORD PTR [rsp+0x230],xmm15
  e02465:	00 00 
  e02467:	44 0f 11 bc 24 40 02 	movups XMMWORD PTR [rsp+0x240],xmm15
  e0246e:	00 00 
  e02470:	44 0f 11 bc 24 50 02 	movups XMMWORD PTR [rsp+0x250],xmm15
  e02477:	00 00 
  e02479:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e02480:	00 
  e02481:	48 8b 51 40          	mov    rdx,QWORD PTR [rcx+0x40]
  e02485:	48 89 94 24 68 01 00 	mov    QWORD PTR [rsp+0x168],rdx
  e0248c:	00 
  e0248d:	48 8d 94 24 28 02 00 	lea    rdx,[rsp+0x228]
  e02494:	00 
  e02495:	48 89 94 24 70 01 00 	mov    QWORD PTR [rsp+0x170],rdx
  e0249c:	00 
  e0249d:	48 8b 94 24 68 01 00 	mov    rdx,QWORD PTR [rsp+0x168]
  e024a4:	00 
  e024a5:	48 85 d2             	test   rdx,rdx
  e024a8:	74 09                	je     e024b3 <crosscall2@@Base+0x85a393>
  e024aa:	48 8d 05 27 53 d8 00 	lea    rax,[rip+0xd85327]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e024b1:	eb 04                	jmp    e024b7 <crosscall2@@Base+0x85a397>
  e024b3:	31 c0                	xor    eax,eax
  e024b5:	31 d2                	xor    edx,edx
  e024b7:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e024be:	00 
  e024bf:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e024c6:	00 
  e024c7:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e024ce:	00 
  e024cf:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e024d3:	48 8d 05 26 55 8d 00 	lea    rax,[rip+0x8d5526]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e024da:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e024e1:	00 
  e024e2:	e8 19 3c 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e024e7:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e024ec:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e024f0:	83 3d b9 76 af 01 00 	cmp    DWORD PTR [rip+0x1af76b9],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e024f7:	75 12                	jne    e0250b <crosscall2@@Base+0x85a3eb>
  e024f9:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e02500:	00 
  e02501:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e02508:	00 
  e02509:	eb 27                	jmp    e02532 <crosscall2@@Base+0x85a412>
  e0250b:	e8 b0 0c 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e02510:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e02517:	00 
  e02518:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e0251b:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e0251e:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e02522:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e02529:	00 
  e0252a:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e0252e:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e02532:	48 89 08             	mov    QWORD PTR [rax],rcx
  e02535:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e0253c:	00 
  e0253d:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e02541:	48 8d 05 d8 55 8d 00 	lea    rax,[rip+0x8d55d8]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e02548:	e8 d3 4b 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e0254d:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e02554:	00 
  e02555:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02559:	48 8d 05 e0 56 8d 00 	lea    rax,[rip+0x8d56e0]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e02560:	e8 bb 4b 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02565:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e0256c:	00 
  e0256d:	48 8b 51 48          	mov    rdx,QWORD PTR [rcx+0x48]
  e02571:	48 89 94 24 58 01 00 	mov    QWORD PTR [rsp+0x158],rdx
  e02578:	00 
  e02579:	48 8d 94 24 d8 00 00 	lea    rdx,[rsp+0xd8]
  e02580:	00 
  e02581:	48 89 94 24 60 01 00 	mov    QWORD PTR [rsp+0x160],rdx
  e02588:	00 
  e02589:	48 8b 94 24 58 01 00 	mov    rdx,QWORD PTR [rsp+0x158]
  e02590:	00 
  e02591:	48 85 d2             	test   rdx,rdx
  e02594:	74 09                	je     e0259f <crosscall2@@Base+0x85a47f>
  e02596:	48 8d 05 3b 52 d8 00 	lea    rax,[rip+0xd8523b]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e0259d:	eb 04                	jmp    e025a3 <crosscall2@@Base+0x85a483>
  e0259f:	31 c0                	xor    eax,eax
  e025a1:	31 d2                	xor    edx,edx
  e025a3:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e025aa:	00 
  e025ab:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e025b2:	00 
  e025b3:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e025ba:	00 
  e025bb:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e025bf:	48 8d 05 3a 54 8d 00 	lea    rax,[rip+0x8d543a]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e025c6:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e025cd:	00 
  e025ce:	e8 2d 3b 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e025d3:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e025d8:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e025dc:	83 3d cd 75 af 01 00 	cmp    DWORD PTR [rip+0x1af75cd],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e025e3:	75 12                	jne    e025f7 <crosscall2@@Base+0x85a4d7>
  e025e5:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e025ec:	00 
  e025ed:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e025f4:	00 
  e025f5:	eb 27                	jmp    e0261e <crosscall2@@Base+0x85a4fe>
  e025f7:	e8 c4 0b 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e025fc:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e02603:	00 
  e02604:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e02607:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e0260a:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e0260e:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e02615:	00 
  e02616:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e0261a:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e0261e:	48 89 08             	mov    QWORD PTR [rax],rcx
  e02621:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e02628:	00 
  e02629:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e0262d:	48 8d 05 ec 54 8d 00 	lea    rax,[rip+0x8d54ec]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e02634:	e8 e7 4a 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02639:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e02640:	00 
  e02641:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02645:	48 8d 05 f4 55 8d 00 	lea    rax,[rip+0x8d55f4]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e0264c:	e8 cf 4a 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02651:	44 0f 11 7c 24 70    	movups XMMWORD PTR [rsp+0x70],xmm15
  e02657:	48 c7 84 24 80 00 00 	mov    QWORD PTR [rsp+0x80],0x0
  e0265e:	00 00 00 00 00 
  e02663:	44 0f 11 bc 24 10 02 	movups XMMWORD PTR [rsp+0x210],xmm15
  e0266a:	00 00 
  e0266c:	48 c7 84 24 20 02 00 	mov    QWORD PTR [rsp+0x220],0x0
  e02673:	00 00 00 00 00 
  e02678:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e0267f:	00 
  e02680:	48 8b 51 50          	mov    rdx,QWORD PTR [rcx+0x50]
  e02684:	48 89 94 24 48 01 00 	mov    QWORD PTR [rsp+0x148],rdx
  e0268b:	00 
  e0268c:	48 8d 94 24 10 02 00 	lea    rdx,[rsp+0x210]
  e02693:	00 
  e02694:	48 89 94 24 50 01 00 	mov    QWORD PTR [rsp+0x150],rdx
  e0269b:	00 
  e0269c:	48 8b 94 24 48 01 00 	mov    rdx,QWORD PTR [rsp+0x148]
  e026a3:	00 
  e026a4:	48 85 d2             	test   rdx,rdx
  e026a7:	74 09                	je     e026b2 <crosscall2@@Base+0x85a592>
  e026a9:	48 8d 05 28 51 d8 00 	lea    rax,[rip+0xd85128]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e026b0:	eb 04                	jmp    e026b6 <crosscall2@@Base+0x85a596>
  e026b2:	31 c0                	xor    eax,eax
  e026b4:	31 d2                	xor    edx,edx
  e026b6:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e026bd:	00 
  e026be:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e026c5:	00 
  e026c6:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e026cd:	00 
  e026ce:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e026d2:	48 8d 05 27 53 8d 00 	lea    rax,[rip+0x8d5327]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e026d9:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e026e0:	00 
  e026e1:	e8 1a 3a 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e026e6:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e026eb:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e026ef:	83 3d ba 74 af 01 00 	cmp    DWORD PTR [rip+0x1af74ba],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e026f6:	75 12                	jne    e0270a <crosscall2@@Base+0x85a5ea>
  e026f8:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e026ff:	00 
  e02700:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e02707:	00 
  e02708:	eb 27                	jmp    e02731 <crosscall2@@Base+0x85a611>
  e0270a:	e8 b1 0a 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e0270f:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e02716:	00 
  e02717:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e0271a:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e0271d:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e02721:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e02728:	00 
  e02729:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e0272d:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e02731:	48 89 08             	mov    QWORD PTR [rax],rcx
  e02734:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e0273b:	00 
  e0273c:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e02740:	48 8d 05 d9 53 8d 00 	lea    rax,[rip+0x8d53d9]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e02747:	e8 d4 49 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e0274c:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e02753:	00 
  e02754:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02758:	48 8d 05 e1 54 8d 00 	lea    rax,[rip+0x8d54e1]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e0275f:	90                   	nop
  e02760:	e8 bb 49 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02765:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e0276c:	00 
  e0276d:	48 8b 51 58          	mov    rdx,QWORD PTR [rcx+0x58]
  e02771:	48 89 94 24 38 01 00 	mov    QWORD PTR [rsp+0x138],rdx
  e02778:	00 
  e02779:	48 8d 54 24 70       	lea    rdx,[rsp+0x70]
  e0277e:	48 89 94 24 40 01 00 	mov    QWORD PTR [rsp+0x140],rdx
  e02785:	00 
  e02786:	48 8b 94 24 38 01 00 	mov    rdx,QWORD PTR [rsp+0x138]
  e0278d:	00 
  e0278e:	48 85 d2             	test   rdx,rdx
  e02791:	74 09                	je     e0279c <crosscall2@@Base+0x85a67c>
  e02793:	48 8d 05 3e 50 d8 00 	lea    rax,[rip+0xd8503e]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e0279a:	eb 04                	jmp    e027a0 <crosscall2@@Base+0x85a680>
  e0279c:	31 c0                	xor    eax,eax
  e0279e:	31 d2                	xor    edx,edx
  e027a0:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e027a7:	00 
  e027a8:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e027af:	00 
  e027b0:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e027b7:	00 
  e027b8:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e027bc:	48 8d 05 3d 52 8d 00 	lea    rax,[rip+0x8d523d]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e027c3:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e027ca:	00 
  e027cb:	e8 30 39 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e027d0:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e027d5:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e027d9:	83 3d d0 73 af 01 00 	cmp    DWORD PTR [rip+0x1af73d0],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e027e0:	75 12                	jne    e027f4 <crosscall2@@Base+0x85a6d4>
  e027e2:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e027e9:	00 
  e027ea:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e027f1:	00 
  e027f2:	eb 27                	jmp    e0281b <crosscall2@@Base+0x85a6fb>
  e027f4:	e8 c7 09 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e027f9:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e02800:	00 
  e02801:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e02804:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e02807:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e0280b:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e02812:	00 
  e02813:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e02817:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e0281b:	48 89 08             	mov    QWORD PTR [rax],rcx
  e0281e:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e02825:	00 
  e02826:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e0282a:	48 8d 05 ef 52 8d 00 	lea    rax,[rip+0x8d52ef]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e02831:	e8 ea 48 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02836:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e0283d:	00 
  e0283e:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02842:	48 8d 05 f7 53 8d 00 	lea    rax,[rip+0x8d53f7]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e02849:	e8 d2 48 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e0284e:	44 0f 11 bc 24 88 00 	movups XMMWORD PTR [rsp+0x88],xmm15
  e02855:	00 00 
  e02857:	48 c7 84 24 98 00 00 	mov    QWORD PTR [rsp+0x98],0x0
  e0285e:	00 00 00 00 00 
  e02863:	44 0f 11 bc 24 f8 01 	movups XMMWORD PTR [rsp+0x1f8],xmm15
  e0286a:	00 00 
  e0286c:	48 c7 84 24 08 02 00 	mov    QWORD PTR [rsp+0x208],0x0
  e02873:	00 00 00 00 00 
  e02878:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e0287f:	00 
  e02880:	48 8b 51 60          	mov    rdx,QWORD PTR [rcx+0x60]
  e02884:	48 89 94 24 28 01 00 	mov    QWORD PTR [rsp+0x128],rdx
  e0288b:	00 
  e0288c:	48 8d 94 24 f8 01 00 	lea    rdx,[rsp+0x1f8]
  e02893:	00 
  e02894:	48 89 94 24 30 01 00 	mov    QWORD PTR [rsp+0x130],rdx
  e0289b:	00 
  e0289c:	48 8b 94 24 28 01 00 	mov    rdx,QWORD PTR [rsp+0x128]
  e028a3:	00 
  e028a4:	48 85 d2             	test   rdx,rdx
  e028a7:	74 09                	je     e028b2 <crosscall2@@Base+0x85a792>
  e028a9:	48 8d 05 28 4f d8 00 	lea    rax,[rip+0xd84f28]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e028b0:	eb 04                	jmp    e028b6 <crosscall2@@Base+0x85a796>
  e028b2:	31 c0                	xor    eax,eax
  e028b4:	31 d2                	xor    edx,edx
  e028b6:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e028bd:	00 
  e028be:	48 89 94 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rdx
  e028c5:	00 
  e028c6:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e028cd:	00 
  e028ce:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e028d2:	48 8d 05 27 51 8d 00 	lea    rax,[rip+0x8d5127]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e028d9:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e028e0:	00 
  e028e1:	e8 1a 38 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e028e6:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e028eb:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e028ef:	83 3d ba 72 af 01 00 	cmp    DWORD PTR [rip+0x1af72ba],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e028f6:	75 12                	jne    e0290a <crosscall2@@Base+0x85a7ea>
  e028f8:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e028ff:	00 
  e02900:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e02907:	00 
  e02908:	eb 27                	jmp    e02931 <crosscall2@@Base+0x85a811>
  e0290a:	e8 b1 08 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e0290f:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e02916:	00 
  e02917:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e0291a:	48 8b 30             	mov    rsi,QWORD PTR [rax]
  e0291d:	49 89 73 08          	mov    QWORD PTR [r11+0x8],rsi
  e02921:	48 8b b4 24 f0 02 00 	mov    rsi,QWORD PTR [rsp+0x2f0]
  e02928:	00 
  e02929:	48 8b 7e 20          	mov    rdi,QWORD PTR [rsi+0x20]
  e0292d:	49 89 7b 10          	mov    QWORD PTR [r11+0x10],rdi
  e02931:	48 89 08             	mov    QWORD PTR [rax],rcx
  e02934:	48 c7 46 20 00 00 00 	mov    QWORD PTR [rsi+0x20],0x0
  e0293b:	00 
  e0293c:	48 8b 5e 28          	mov    rbx,QWORD PTR [rsi+0x28]
  e02940:	48 8d 05 d9 51 8d 00 	lea    rax,[rip+0x8d51d9]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e02947:	e8 d4 47 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e0294c:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e02953:	00 
  e02954:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02958:	48 8d 05 e1 52 8d 00 	lea    rax,[rip+0x8d52e1]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e0295f:	90                   	nop
  e02960:	e8 bb 47 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02965:	48 8b 8c 24 e8 02 00 	mov    rcx,QWORD PTR [rsp+0x2e8]
  e0296c:	00 
  e0296d:	48 8b 49 68          	mov    rcx,QWORD PTR [rcx+0x68]
  e02971:	48 89 8c 24 18 01 00 	mov    QWORD PTR [rsp+0x118],rcx
  e02978:	00 
  e02979:	48 8d 8c 24 88 00 00 	lea    rcx,[rsp+0x88]
  e02980:	00 
  e02981:	48 89 8c 24 20 01 00 	mov    QWORD PTR [rsp+0x120],rcx
  e02988:	00 
  e02989:	48 8b 8c 24 18 01 00 	mov    rcx,QWORD PTR [rsp+0x118]
  e02990:	00 
  e02991:	48 85 c9             	test   rcx,rcx
  e02994:	74 09                	je     e0299f <crosscall2@@Base+0x85a87f>
  e02996:	48 8d 05 3b 4e d8 00 	lea    rax,[rip+0xd84e3b]        # 1b877d8 <cbPAMConv@@Base+0x618628>
  e0299d:	eb 04                	jmp    e029a3 <crosscall2@@Base+0x85a883>
  e0299f:	31 c0                	xor    eax,eax
  e029a1:	31 c9                	xor    ecx,ecx
  e029a3:	48 89 84 24 c8 02 00 	mov    QWORD PTR [rsp+0x2c8],rax
  e029aa:	00 
  e029ab:	48 89 8c 24 d0 02 00 	mov    QWORD PTR [rsp+0x2d0],rcx
  e029b2:	00 
  e029b3:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e029ba:	00 
  e029bb:	48 8b 5a 10          	mov    rbx,QWORD PTR [rdx+0x10]
  e029bf:	48 8d 05 3a 50 8d 00 	lea    rax,[rip+0x8d503a]        # 16d7a00 <cbPAMConv@@Base+0x168850>
  e029c6:	48 8d 8c 24 c8 02 00 	lea    rcx,[rsp+0x2c8]
  e029cd:	00 
  e029ce:	e8 2d 37 67 ff       	call   476100 <pam_start_confdir@plt+0x704e8>
  e029d3:	48 8b 54 24 30       	mov    rdx,QWORD PTR [rsp+0x30]
  e029d8:	48 89 50 08          	mov    QWORD PTR [rax+0x8],rdx
  e029dc:	83 3d cd 71 af 01 00 	cmp    DWORD PTR [rip+0x1af71cd],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e029e3:	75 12                	jne    e029f7 <crosscall2@@Base+0x85a8d7>
  e029e5:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e029ec:	00 
  e029ed:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e029f4:	00 
  e029f5:	eb 27                	jmp    e02a1e <crosscall2@@Base+0x85a8fe>
  e029f7:	e8 c4 07 68 ff       	call   4831c0 <_cgo_topofstack@@Base+0xa0>
  e029fc:	48 8b 8c 24 10 01 00 	mov    rcx,QWORD PTR [rsp+0x110]
  e02a03:	00 
  e02a04:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e02a07:	48 8b 10             	mov    rdx,QWORD PTR [rax]
  e02a0a:	49 89 53 08          	mov    QWORD PTR [r11+0x8],rdx
  e02a0e:	48 8b 94 24 f0 02 00 	mov    rdx,QWORD PTR [rsp+0x2f0]
  e02a15:	00 
  e02a16:	48 8b 72 20          	mov    rsi,QWORD PTR [rdx+0x20]
  e02a1a:	49 89 73 10          	mov    QWORD PTR [r11+0x10],rsi
  e02a1e:	48 89 08             	mov    QWORD PTR [rax],rcx
  e02a21:	48 c7 42 20 00 00 00 	mov    QWORD PTR [rdx+0x20],0x0
  e02a28:	00 
  e02a29:	48 8b 5a 28          	mov    rbx,QWORD PTR [rdx+0x28]
  e02a2d:	48 8d 05 ec 50 8d 00 	lea    rax,[rip+0x8d50ec]        # 16d7b20 <cbPAMConv@@Base+0x168970>
  e02a34:	e8 e7 46 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02a39:	48 8b 8c 24 f0 02 00 	mov    rcx,QWORD PTR [rsp+0x2f0]
  e02a40:	00 
  e02a41:	48 8b 59 30          	mov    rbx,QWORD PTR [rcx+0x30]
  e02a45:	48 8d 05 f4 51 8d 00 	lea    rax,[rip+0x8d51f4]        # 16d7c40 <cbPAMConv@@Base+0x168a90>
  e02a4c:	e8 cf 46 67 ff       	call   477120 <pam_start_confdir@plt+0x71508>
  e02a51:	48 81 c4 d8 02 00 00 	add    rsp,0x2d8
  e02a58:	5d                   	pop    rbp
  e02a59:	c3                   	ret
  e02a5a:	48 89 44 24 08       	mov    QWORD PTR [rsp+0x8],rax
  e02a5f:	48 89 5c 24 10       	mov    QWORD PTR [rsp+0x10],rbx
  e02a64:	48 89 4c 24 18       	mov    QWORD PTR [rsp+0x18],rcx
  e02a69:	48 89 7c 24 20       	mov    QWORD PTR [rsp+0x20],rdi
  e02a6e:	e8 2d e8 67 ff       	call   4812a0 <pam_start_confdir@plt+0x7b688>
  e02a73:	48 8b 44 24 08       	mov    rax,QWORD PTR [rsp+0x8]
  e02a78:	48 8b 5c 24 10       	mov    rbx,QWORD PTR [rsp+0x10]
  e02a7d:	48 8b 4c 24 18       	mov    rcx,QWORD PTR [rsp+0x18]
  e02a82:	48 8b 7c 24 20       	mov    rdi,QWORD PTR [rsp+0x20]
  e02a87:	e9 34 f1 ff ff       	jmp    e01bc0 <crosscall2@@Base+0x859aa0>
  e02a8c:	cc                   	int3
  e02a8d:	cc                   	int3
  e02a8e:	cc                   	int3
  e02a8f:	cc                   	int3
  e02a90:	cc                   	int3
  e02a91:	cc                   	int3
  e02a92:	cc                   	int3
  e02a93:	cc                   	int3
  e02a94:	cc                   	int3
  e02a95:	cc                   	int3
  e02a96:	cc                   	int3
  e02a97:	cc                   	int3
  e02a98:	cc                   	int3
  e02a99:	cc                   	int3
  e02a9a:	cc                   	int3
  e02a9b:	cc                   	int3
  e02a9c:	cc                   	int3
  e02a9d:	cc                   	int3
  e02a9e:	cc                   	int3
  e02a9f:	cc                   	int3
  e02aa0:	49 3b 66 10          	cmp    rsp,QWORD PTR [r14+0x10]
  e02aa4:	76 32                	jbe    e02ad8 <crosscall2@@Base+0x85a9b8>
  e02aa6:	55                   	push   rbp
  e02aa7:	48 89 e5             	mov    rbp,rsp
  e02aaa:	48 83 ec 10          	sub    rsp,0x10
  e02aae:	4d 8b 66 20          	mov    r12,QWORD PTR [r14+0x20]
  e02ab2:	4d 85 e4             	test   r12,r12
  e02ab5:	75 28                	jne    e02adf <crosscall2@@Base+0x85a9bf>
  e02ab7:	48 8d 05 62 95 7f 00 	lea    rax,[rip+0x7f9562]        # 15fc020 <cbPAMConv@@Base+0x8ce70>
  e02abe:	66 90                	xchg   ax,ax
  e02ac0:	e8 bb 3e 61 ff       	call   416980 <pam_start_confdir@plt+0x10d68>
  e02ac5:	48 8d 0d 34 2b 82 00 	lea    rcx,[rip+0x822b34]        # 1625600 <cbPAMConv@@Base+0xb6450>
  e02acc:	48 89 c3             	mov    rbx,rax
  e02acf:	48 89 c8             	mov    rax,rcx
  e02ad2:	48 83 c4 10          	add    rsp,0x10
  e02ad6:	5d                   	pop    rbp
  e02ad7:	c3                   	ret
  e02ad8:	e8 c3 e7 67 ff       	call   4812a0 <pam_start_confdir@plt+0x7b688>
  e02add:	eb c1                	jmp    e02aa0 <crosscall2@@Base+0x85a980>
  e02adf:	4c 8d 6c 24 20       	lea    r13,[rsp+0x20]
  e02ae4:	4d 39 2c 24          	cmp    QWORD PTR [r12],r13
  e02ae8:	75 cd                	jne    e02ab7 <crosscall2@@Base+0x85a997>
  e02aea:	49 89 24 24          	mov    QWORD PTR [r12],rsp
  e02aee:	eb c7                	jmp    e02ab7 <crosscall2@@Base+0x85a997>
  e02af0:	cc                   	int3
  e02af1:	cc                   	int3
  e02af2:	cc                   	int3
  e02af3:	cc                   	int3
  e02af4:	cc                   	int3
  e02af5:	cc                   	int3
  e02af6:	cc                   	int3
  e02af7:	cc                   	int3
  e02af8:	cc                   	int3
  e02af9:	cc                   	int3
  e02afa:	cc                   	int3
  e02afb:	cc                   	int3
  e02afc:	cc                   	int3
  e02afd:	cc                   	int3
  e02afe:	cc                   	int3
  e02aff:	cc                   	int3
  e02b00:	55                   	push   rbp
  e02b01:	48 89 e5             	mov    rbp,rsp
  e02b04:	48 83 ec 10          	sub    rsp,0x10
  e02b08:	4d 8b 66 20          	mov    r12,QWORD PTR [r14+0x20]
  e02b0c:	4d 85 e4             	test   r12,r12
  e02b0f:	75 2a                	jne    e02b3b <crosscall2@@Base+0x85aa1b>
  e02b11:	48 89 44 24 20       	mov    QWORD PTR [rsp+0x20],rax
  e02b16:	48 39 fb             	cmp    rbx,rdi
  e02b19:	76 14                	jbe    e02b2f <crosscall2@@Base+0x85aa0f>
  e02b1b:	48 8d 0d de 2a 82 00 	lea    rcx,[rip+0x822ade]        # 1625600 <cbPAMConv@@Base+0xb6450>
  e02b22:	48 8d 1c f8          	lea    rbx,[rax+rdi*8]
  e02b26:	48 89 c8             	mov    rax,rcx
  e02b29:	48 83 c4 10          	add    rsp,0x10
  e02b2d:	5d                   	pop    rbp
  e02b2e:	c3                   	ret
  e02b2f:	48 89 f8             	mov    rax,rdi
  e02b32:	48 89 d9             	mov    rcx,rbx
  e02b35:	e8 06 0a 68 ff       	call   483540 <_cgo_topofstack@@Base+0x420>
  e02b3a:	90                   	nop
  e02b3b:	4c 8d 6c 24 20       	lea    r13,[rsp+0x20]
  e02b40:	4d 39 2c 24          	cmp    QWORD PTR [r12],r13
  e02b44:	75 cb                	jne    e02b11 <crosscall2@@Base+0x85a9f1>
  e02b46:	49 89 24 24          	mov    QWORD PTR [r12],rsp
  e02b4a:	eb c5                	jmp    e02b11 <crosscall2@@Base+0x85a9f1>
  e02b4c:	cc                   	int3
  e02b4d:	cc                   	int3
  e02b4e:	cc                   	int3
  e02b4f:	cc                   	int3
  e02b50:	cc                   	int3
  e02b51:	cc                   	int3
  e02b52:	cc                   	int3
  e02b53:	cc                   	int3
  e02b54:	cc                   	int3
  e02b55:	cc                   	int3
  e02b56:	cc                   	int3
  e02b57:	cc                   	int3
  e02b58:	cc                   	int3
  e02b59:	cc                   	int3
  e02b5a:	cc                   	int3
  e02b5b:	cc                   	int3
  e02b5c:	cc                   	int3
  e02b5d:	cc                   	int3
  e02b5e:	cc                   	int3
  e02b5f:	cc                   	int3
  e02b60:	49 3b 66 10          	cmp    rsp,QWORD PTR [r14+0x10]
  e02b64:	0f 86 d2 00 00 00    	jbe    e02c3c <crosscall2@@Base+0x85ab1c>
  e02b6a:	55                   	push   rbp
  e02b6b:	48 89 e5             	mov    rbp,rsp
  e02b6e:	48 83 ec 20          	sub    rsp,0x20
  e02b72:	4d 8b 66 20          	mov    r12,QWORD PTR [r14+0x20]
  e02b76:	4d 85 e4             	test   r12,r12
  e02b79:	0f 85 ef 00 00 00    	jne    e02c6e <crosscall2@@Base+0x85ab4e>
  e02b7f:	48 89 5c 24 38       	mov    QWORD PTR [rsp+0x38],rbx
  e02b84:	48 85 db             	test   rbx,rbx
  e02b87:	74 2d                	je     e02bb6 <crosscall2@@Base+0x85aa96>
  e02b89:	48 89 44 24 30       	mov    QWORD PTR [rsp+0x30],rax
  e02b8e:	48 85 c9             	test   rcx,rcx
  e02b91:	74 1f                	je     e02bb2 <crosscall2@@Base+0x85aa92>
  e02b93:	48 8d 57 ff          	lea    rdx,[rdi-0x1]
  e02b97:	48 f7 da             	neg    rdx
  e02b9a:	48 c1 fa 3f          	sar    rdx,0x3f
  e02b9e:	83 e2 08             	and    edx,0x8
  e02ba1:	48 63 33             	movsxd rsi,DWORD PTR [rbx]
  e02ba4:	48 01 da             	add    rdx,rbx
  e02ba7:	48 8d 79 ff          	lea    rdi,[rcx-0x1]
  e02bab:	31 c9                	xor    ecx,ecx
  e02bad:	e9 80 00 00 00       	jmp    e02c32 <crosscall2@@Base+0x85ab12>
  e02bb2:	31 c9                	xor    ecx,ecx
  e02bb4:	eb 2b                	jmp    e02be1 <crosscall2@@Base+0x85aac1>
  e02bb6:	44 0f 11 78 08       	movups XMMWORD PTR [rax+0x8],xmm15
  e02bbb:	83 3d ee 6f af 01 00 	cmp    DWORD PTR [rip+0x1af6fee],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e02bc2:	74 0b                	je     e02bcf <crosscall2@@Base+0x85aaaf>
  e02bc4:	48 8b 08             	mov    rcx,QWORD PTR [rax]
  e02bc7:	e8 b4 05 68 ff       	call   483180 <_cgo_topofstack@@Base+0x60>
  e02bcc:	49 89 0b             	mov    QWORD PTR [r11],rcx
  e02bcf:	48 c7 00 00 00 00 00 	mov    QWORD PTR [rax],0x0
  e02bd6:	31 c0                	xor    eax,eax
  e02bd8:	31 db                	xor    ebx,ebx
  e02bda:	48 83 c4 20          	add    rsp,0x20
  e02bde:	5d                   	pop    rbp
  e02bdf:	90                   	nop
  e02be0:	c3                   	ret
  e02be1:	48 89 4c 24 18       	mov    QWORD PTR [rsp+0x18],rcx
  e02be6:	48 8d 05 33 94 7f 00 	lea    rax,[rip+0x7f9433]        # 15fc020 <cbPAMConv@@Base+0x8ce70>
  e02bed:	48 89 cb             	mov    rbx,rcx
  e02bf0:	e8 8b a2 67 ff       	call   47ce80 <pam_start_confdir@plt+0x77268>
  e02bf5:	48 8b 54 24 18       	mov    rdx,QWORD PTR [rsp+0x18]
  e02bfa:	48 8b 74 24 30       	mov    rsi,QWORD PTR [rsp+0x30]
  e02bff:	48 89 56 08          	mov    QWORD PTR [rsi+0x8],rdx
  e02c03:	48 89 56 10          	mov    QWORD PTR [rsi+0x10],rdx
  e02c07:	83 3d a2 6f af 01 00 	cmp    DWORD PTR [rip+0x1af6fa2],0x0        # 28f9bb0 <cbPAMConv@@Base+0x138aa00>
  e02c0e:	74 0f                	je     e02c1f <crosscall2@@Base+0x85aaff>
  e02c10:	e8 8b 05 68 ff       	call   4831a0 <_cgo_topofstack@@Base+0x80>
  e02c15:	49 89 03             	mov    QWORD PTR [r11],rax
  e02c18:	48 8b 0e             	mov    rcx,QWORD PTR [rsi]
  e02c1b:	49 89 4b 08          	mov    QWORD PTR [r11+0x8],rcx
  e02c1f:	48 89 06             	mov    QWORD PTR [rsi],rax
  e02c22:	eb b2                	jmp    e02bd6 <crosscall2@@Base+0x85aab6>
  e02c24:	4c 8d 04 ca          	lea    r8,[rdx+rcx*8]
  e02c28:	4d 63 00             	movsxd r8,DWORD PTR [r8]
  e02c2b:	48 ff c1             	inc    rcx
  e02c2e:	49 0f af f0          	imul   rsi,r8
  e02c32:	48 39 f9             	cmp    rcx,rdi
  e02c35:	7c ed                	jl     e02c24 <crosscall2@@Base+0x85ab04>
  e02c37:	48 89 f1             	mov    rcx,rsi
  e02c3a:	eb a5                	jmp    e02be1 <crosscall2@@Base+0x85aac1>
  e02c3c:	48 89 44 24 08       	mov    QWORD PTR [rsp+0x8],rax
  e02c41:	48 89 5c 24 10       	mov    QWORD PTR [rsp+0x10],rbx
  e02c46:	48 89 4c 24 18       	mov    QWORD PTR [rsp+0x18],rcx
  e02c4b:	48 89 7c 24 20       	mov    QWORD PTR [rsp+0x20],rdi
  e02c50:	e8 4b e6 67 ff       	call   4812a0 <pam_start_confdir@plt+0x7b688>
  e02c55:	48 8b 44 24 08       	mov    rax,QWORD PTR [rsp+0x8]
  e02c5a:	48 8b 5c 24 10       	mov    rbx,QWORD PTR [rsp+0x10]
  e02c5f:	48 8b 4c 24 18       	mov    rcx,QWORD PTR [rsp+0x18]
  e02c64:	48 8b 7c 24 20       	mov    rdi,QWORD PTR [rsp+0x20]
  e02c69:	e9 f2 fe ff ff       	jmp    e02b60 <crosscall2@@Base+0x85aa40>
  e02c6e:	4c 8d 6c 24 30       	lea    r13,[rsp+0x30]
  e02c73:	4d 39 2c 24          	cmp    QWORD PTR [r12],r13
  e02c77:	0f 85 02 ff ff ff    	jne    e02b7f <crosscall2@@Base+0x85aa5f>
  e02c7d:	49 89 24 24          	mov    QWORD PTR [r12],rsp
  e02c81:	e9 f9 fe ff ff       	jmp    e02b7f <crosscall2@@Base+0x85aa5f>
  e02c86:	cc                   	int3
  e02c87:	cc                   	int3
  e02c88:	cc                   	int3
  e02c89:	cc                   	int3
  e02c8a:	cc                   	int3
  e02c8b:	cc                   	int3
  e02c8c:	cc                   	int3
  e02c8d:	cc                   	int3
  e02c8e:	cc                   	int3
  e02c8f:	cc                   	int3
  e02c90:	cc                   	int3
  e02c91:	cc                   	int3
  e02c92:	cc                   	int3
  e02c93:	cc                   	int3
  e02c94:	cc                   	int3
  e02c95:	cc                   	int3
  e02c96:	cc                   	int3
  e02c97:	cc                   	int3
  e02c98:	cc                   	int3
  e02c99:	cc                   	int3
  e02c9a:	cc                   	int3
  e02c9b:	cc                   	int3
  e02c9c:	cc                   	int3
  e02c9d:	cc                   	int3
  e02c9e:	cc                   	int3
  e02c9f:	cc                   	int3
  e02ca0:	4d 8b 66 20          	mov    r12,QWORD PTR [r14+0x20]
  e02ca4:	4d 85 e4             	test   r12,r12
  e02ca7:	75 0b                	jne    e02cb4 <crosscall2@@Base+0x85ab94>
  e02ca9:	90                   	nop
  e02caa:	48 8d 05 6f 93 7f 00 	lea    rax,[rip+0x7f936f]        # 15fc020 <cbPAMConv@@Base+0x8ce70>
  e02cb1:	31 db                	xor    ebx,ebx
  e02cb3:	c3                   	ret
  e02cb4:	4c 8d 6c 24 08       	lea    r13,[rsp+0x8]
  e02cb9:	4d 39 2c 24          	cmp    QWORD PTR [r12],r13
  e02cbd:	75 ea                	jne    e02ca9 <crosscall2@@Base+0x85ab89>
  e02cbf:	49 89 24 24          	mov    QWORD PTR [r12],rsp
  e02cc3:	eb e4                	jmp    e02ca9 <crosscall2@@Base+0x85ab89>
  e02cc5:	cc                   	int3
  e02cc6:	cc                   	int3
  e02cc7:	cc                   	int3
  e02cc8:	cc                   	int3
  e02cc9:	cc                   	int3
  e02cca:	cc                   	int3
  e02ccb:	cc                   	int3
  e02ccc:	cc                   	int3
  e02ccd:	cc                   	int3
  e02cce:	cc                   	int3
  e02ccf:	cc                   	int3
  e02cd0:	cc                   	int3
  e02cd1:	cc                   	int3
  e02cd2:	cc                   	int3
  e02cd3:	cc                   	int3
  e02cd4:	cc                   	int3
  e02cd5:	cc                   	int3
  e02cd6:	cc                   	int3
  e02cd7:	cc                   	int3
  e02cd8:	cc                   	int3
  e02cd9:	cc                   	int3
  e02cda:	cc                   	int3
  e02cdb:	cc                   	int3
  e02cdc:	cc                   	int3
  e02cdd:	cc                   	int3
  e02cde:	cc                   	int3
  e02cdf:	cc                   	int3
  e02ce0:	55                   	push   rbp
  e02ce1:	48 89 e5             	mov    rbp,rsp
  e02ce4:	48 83 ec 10          	sub    rsp,0x10
  e02ce8:	4d 8b 66 20          	mov    r12,QWORD PTR [r14+0x20]
  e02cec:	4d 85 e4             	test   r12,r12
  e02cef:	75 27                	jne    e02d18 <crosscall2@@Base+0x85abf8>
  e02cf1:	48 89 44 24 20       	mov    QWORD PTR [rsp+0x20],rax
  e02cf6:	48 39 fb             	cmp    rbx,rdi
  e02cf9:	76 11                	jbe    e02d0c <crosscall2@@Base+0x85abec>
  e02cfb:	48 8b 1c f8          	mov    rbx,QWORD PTR [rax+rdi*8]
  e02cff:	48 8d 05 1a 93 7f 00 	lea    rax,[rip+0x7f931a]        # 15fc020 <cbPAMConv@@Base+0x8ce70>
  e02d06:	48 83 c4 10          	add    rsp,0x10
  e02d0a:	5d                   	pop    rbp
  e02d0b:	c3                   	ret
  e02d0c:	48 89 f8             	mov    rax,rdi
  e02d0f:	48 89 d9             	mov    rcx,rbx
  e02d12:	e8 29 08 68 ff       	call   483540 <_cgo_topofstack@@Base+0x420>
  e02d17:	90                   	nop
  e02d18:	4c 8d 6c 24 20       	lea    r13,[rsp+0x20]
  e02d1d:	0f 1f 00             	nop    DWORD PTR [rax]
  e02d20:	4d 39 2c 24          	cmp    QWORD PTR [r12],r13
  e02d24:	75 cb                	jne    e02cf1 <crosscall2@@Base+0x85abd1>
  e02d26:	49 89 24 24          	mov    QWORD PTR [r12],rsp
  e02d2a:	eb c5                	jmp    e02cf1 <crosscall2@@Base+0x85abd1>
  e02d2c:	cc                   	int3
  e02d2d:	cc                   	int3
  e02d2e:	cc                   	int3
  e02d2f:	cc                   	int3
  e02d30:	cc                   	int3
  e02d31:	cc                   	int3
  e02d32:	cc                   	int3
  e02d33:	cc                   	int3
  e02d34:	cc                   	int3
  e02d35:	cc                   	int3
  e02d36:	cc                   	int3
  e02d37:	cc                   	int3
  e02d38:	cc                   	int3
  e02d39:	cc                   	int3
  e02d3a:	cc                   	int3
  e02d3b:	cc                   	int3
  e02d3c:	cc                   	int3
  e02d3d:	cc                   	int3
  e02d3e:	cc                   	int3
  e02d3f:	cc                   	int3
  e02d40:	49 3b 66 10          	cmp    rsp,QWORD PTR [r14+0x10]
  e02d44:	76 5b                	jbe    e02da1 <crosscall2@@Base+0x85ac81>
  e02d46:	55                   	push   rbp
  e02d47:	48 89 e5             	mov    rbp,rsp
  e02d4a:	48 83 ec 10          	sub    rsp,0x10
  e02d4e:	4d 8b 66 20          	mov    r12,QWORD PTR [r14+0x20]
  e02d52:	4d 85 e4             	test   r12,r12
  e02d55:	75 72                	jne    e02dc9 <crosscall2@@Base+0x85aca9>
  e02d57:	48 89 44 24 20       	mov    QWORD PTR [rsp+0x20],rax
  e02d5c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
  e02d60:	48 85 c0             	test   rax,rax
  e02d63:	75 06                	jne    e02d6b <crosscall2@@Base+0x85ac4b>
  e02d65:	31 c0                	xor    eax,eax
  e02d67:	31 c9                	xor    ecx,ecx
  e02d69:	eb 27                	jmp    e02d92 <crosscall2@@Base+0x85ac72>
  e02d6b:	48 89 5c 24 28       	mov    QWORD PTR [rsp+0x28],rbx
  e02d70:	48 8d 05 89 73 88 00 	lea    rax,[rip+0x887389]        # 168a100 <cbPAMConv@@Base+0x11af50>
  e02d77:	e8 04 3c 61 ff       	call   416980 <pam_start_confdir@plt+0x10d68>
  e02d7c:	48                   	rex.W
  e02d7d:	8b                   	.byte 0x8b
  e02d7e:	4c                   	rex.WR
  e02d7f:	24                   	.byte 0x24
