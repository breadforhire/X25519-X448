
#Internet Research Task Force (IRTF)                           A. Langley
#Request for Comments: 7748                                        Google
#Category: Informational                                       M. Hamburg
#ISSN: 2070-1721                             Rambus Cryptography Research
#                                                              S. Turner
#                                                                 sn3rd
#                                                           January 2016#




a24 = 39081
# curve25519/X25519 a24 = 121665

def decodeUCoordinate(u, bits):
       u_list = [ord(b) for b in u]
       if bits % 8:
           u_list[-1] &= (1<<(bits%8))-1
       return decodeLittleEndian(u_list, bits)

def decodeScalar448(k):
       k_list = [ord(b) for b in k]
       k_list[0] &= 252
       k_list[55] |= 128
       return decodeLittleEndian(k_list, 448)



def cswap(swap, x_2, x_3):
    _mask_swap = 0 - swap
    dummy  = _mask_swap & (x_2 ^ x_3)
    x_2 = x_2 ^ dummy
    x_3 = x_3 ^ dummy
    return (x_2, x_3)

def X448(u, k, bits):
    x_1 = u
    x_2 = 1
    z_2 = 0
    x_3 = u
    z_3 = 1
    swap = 0

    for t in range (bits):
     k_t = (k >> t) & 1
     swap ^= k_t
     (x_2, x_3) = cswap(swap, x_2, x_3)
     (z_2, z_3) = cswap(swap, z_2, z_3)
     swap = k_t

     A = x_2 + z_2
     AA = A * A
     B = x_2 - z_2
     BB = B * B
     E = AA - BB
     C = x_3 + z_3
     D = x_3 - z_3
     DA = D * A
     CB = C * B
     x_3 = (DA + CB) * (DA + CB)
     z_3 = x_1 * ((DA - CB) * (DA - CB))
     x_2 = AA * BB
     z_2 = E * (AA + a24 * E)



