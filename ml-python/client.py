import grpc
import fraud_pb2
import fraud_pb2_grpc

def run():
    # 1. Sunucunun çalıştığı porta bir kanal (channel) açıyoruz
    channel = grpc.insecure_channel('localhost:50051')
    
    # 2. Bu kanal üzerinden iletişim kuracak köprüyü (stub) oluşturuyoruz
    stub = fraud_pb2_grpc.FraudDetectionStub(channel)
    
    print("[CLIENT] Sunucuya 6000 birimlik bir istek gönderiliyor...")
    
    # 3. Sözleşmeye uygun bir istek paketi (TransactionRequest) hazırlıyoruz
    istek = fraud_pb2.TransactionRequest(
        user_id="user_123",
        amount=6000.0,
        location="Istanbul",
        device_id="iphone_13"
    )
    
    # 4. İsteği gönderip cevabı bekliyoruz (Senkron çağrı)
    cevap = stub.CheckTransaction(istek)
    
    # 5. Gelen cevabı ekrana yazdırıyoruz
    print(f"[CLIENT] Gelen Cevap:")
    print(f" - Risk Skoru: {cevap.risk_score}")
    print(f" - Onaylandı mı?: {cevap.is_approved}")
    print(f" - Sebep: {cevap.reason}")

if __name__ == '__main__':
    run()