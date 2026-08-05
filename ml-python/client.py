import grpc
import fraud_pb2
import fraud_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')  # sunucunuzun portunu kullanın
    stub = fraud_pb2_grpc.FraudServiceStub(channel)   # ✅ FraudDetectionStub değil

    istek = fraud_pb2.TransactionRequest(
        transaction_id="tx123",
        amount=6000,
        user_id="user1",
        device_id="device1",
        location="Istanbul"
    )

    print("[CLIENT] Sunucuya 6000 birimlik bir istek gönderiliyor...")
    cevap = stub.CheckTransaction(istek)   # ✅ TransactionResponse dönecek, RiskResponse değil
    print(cevap)

if __name__ == '__main__':
    run()