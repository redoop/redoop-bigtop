package org.apache.ambari.server.license.utils;

import java.io.BufferedReader; 
import java.io.FileReader; 
import java.io.IOException; 
import java.security.InvalidKeyException; 
import java.security.KeyFactory; 
import java.security.NoSuchAlgorithmException; 
import java.security.interfaces.RSAPublicKey; 
import java.security.spec.InvalidKeySpecException; 
import java.security.spec.X509EncodedKeySpec; 

import javax.crypto.BadPaddingException; 
import javax.crypto.Cipher; 
import javax.crypto.IllegalBlockSizeException; 
import javax.crypto.NoSuchPaddingException; 

import com.google.inject.Singleton;

/** 
 * RSA 加密解密类  
 * @author houjinxia  
*/

@Singleton
public class RSAEncrypt {
	 /** 
     * 字节数据转字符串专用集合 
     */  
    private static final char[] HEX_CHAR = { '0', '1', '2', '3', '4', '5', '6',  
            '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f' };
    /** 
     * 从文件中输入流中加载公钥 
     *  
     * @param path
     *            公钥输入流 
     * @throws Exception 
     *             加载公钥时产生的异常 
     */  
    public static String loadPublicKeyByFile(String path) throws Exception {  
        try {  
            BufferedReader br = new BufferedReader(new FileReader(path));  
            String readLine = null;  
            StringBuilder sb = new StringBuilder();  
            while ((readLine = br.readLine()) != null) {  
                sb.append(readLine);  
            }  
            br.close();  
            return sb.toString();  
        } catch (IOException e) {  
            throw new Exception("Public key data read error !");  
        } catch (NullPointerException e) {  
            throw new Exception("Public key input stream is empty !");  
        }  
    }  
  
    /** 
     * 从字符串中加载公钥 
     *  
     * @param publicKeyStr 
     *            公钥数据字符串 
     * @throws Exception 
     *             加载公钥时产生的异常 
     */  
    public static RSAPublicKey loadPublicKeyByStr(String publicKeyStr)  
            throws Exception { 
    	
        try {  
            byte[] buffer = Base64.decode(publicKeyStr);
            KeyFactory keyFactory = KeyFactory.getInstance("RSA");  
            X509EncodedKeySpec keySpec = new X509EncodedKeySpec(buffer);  
            return (RSAPublicKey) keyFactory.generatePublic(keySpec);  
        } catch (NoSuchAlgorithmException e) {  
            throw new Exception("Without this algorithm !");  
        } catch (InvalidKeySpecException e) {  
            throw new Exception("The public key is illegal !");  
        } catch (NullPointerException e) {  
            throw new Exception("Public key data is empty !");  
        }  
    }
    
    /** 
     * 公钥解密过程 
     *  
     * @param publicKey 
     *            公钥 
     * @param cipherData 
     *            密文数据 
     * @return 明文 
     * @throws Exception 
     *             解密过程中的异常信息 
     */  
    public static byte[] decrypt(RSAPublicKey publicKey, byte[] cipherData)  
            throws Exception {  
        if (publicKey == null) {  
            throw new Exception("Public key data is empty !");  
        }  
        Cipher cipher = null;  
        try {  
            // 使用默认RSA  
            cipher = Cipher.getInstance("RSA");  
            // cipher= Cipher.getInstance("RSA", new BouncyCastleProvider());  
            cipher.init(Cipher.DECRYPT_MODE, publicKey);  
            byte[] output = cipher.doFinal(cipherData);  
            return output;  
        } catch (NoSuchAlgorithmException e) {  
            throw new Exception("Without this algorithm !");  
        } catch (NoSuchPaddingException e) {  
            e.printStackTrace();  
            return null;  
        } catch (InvalidKeyException e) {  
            throw new Exception("The public key is illegal !");  
        } catch (IllegalBlockSizeException e) {  
            throw new Exception("Cipher length is illegal");  
        } catch (BadPaddingException e) {  
            throw new Exception("Cipher data has been damaged !");  
        }  
    }  
  
    /** 
     * 字节数据转十六进制字符串 
     *  
     * @param data 
     *            输入数据 
     * @return 十六进制内容 
     */  
    public static String byteArrayToString(byte[] data) {  
        StringBuilder stringBuilder = new StringBuilder();  
        for (int i = 0; i < data.length; i++) {  
            // 取出字节的高四位 作为索引得到相应的十六进制标识符 注意无符号右移  
            stringBuilder.append(HEX_CHAR[(data[i] & 0xf0) >>> 4]);  
            // 取出字节的低四位 作为索引得到相应的十六进制标识符  
            stringBuilder.append(HEX_CHAR[(data[i] & 0x0f)]);  
            if (i < data.length - 1) {  
                stringBuilder.append(' ');  
            }  
        }  
        return stringBuilder.toString();  
    }  

}
