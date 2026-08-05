import grpc
from concurrent import futures
import time

# Otomatik üretilen dosyaları içeri aktarıyoruz
import fraud_pb2
import fraud_pb2_grpc

# 1. Sözleşmedeki servisi miras alan bir sınıf oluşturuyoruz
class FraudServiceServicer(fraud_pb2_grpc.FraudServiceServicer):
    
    # 2. .proto dosyasında tanımladığımız metodu (fonksiyonu) yazıyoruz
    def CheckTransaction(self, request, context):
        print(f"\n[SERVER] İstek alındı! Kullanıcı: {request.user_id}, Tutar: {request.amount}")
        
        # Burada ML modeliniz çalışıp bir tahmin yapacak. Biz şimdilik sahte bir kural yazıyoruz.
        if request.amount > 5000:
            skor = 90.0
            onay = False
            sebep = "Yüksek tutar riski"
        else:
            skor = 15.5
            onay = True
            sebep = "Güvenli işlem"
            
        # 3. Sonucu sözleşmedeki RiskResponse formatına uygun şekilde dönüyoruz
        return fraud_pb2.RiskResponse(
            risk_score=skor,
            is_approved=onay,
            reason=sebep
        )

# 4. Sunucuyu başlatan ana fonksiyon
def serve():
    # Aynı anda birden fazla isteği işleyebilmek için 10 iş parçacıklı bir havuz oluşturuyoruz
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    
    # Kendi yazdığımız sınıfı, gRPC sunucusuna bağlıyoruz
    fraud_pb2_grpc.add_FraudServiceServicer_to_server(FraudServiceServicer(), server)
    
    # Sunucuyu 50051 portunda dinlemeye açıyoruz
    server.add_insecure_port('[::]:50051')
    server.start()
    
    print("[SERVER] gRPC Sunucusu 50051 portunda başlatıldı. Bekleniyor...")
    
    # Sunucunun kapanmamasını, sürekli çalışmasını sağlıyoruz
    server.wait_for_termination()

if __name__ == '__main__':
    serve()