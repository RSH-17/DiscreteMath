class SquareMatrix:
    def __init__(self):
        self.n = 0
        self.mat = [[]]
        self.determinant = None
    
    def setSize(self, n):
        if n <= 0:
            print("행렬의 크기가 0 이하입니다. 다시 설정하십시오.")
        self.n = n
        self.mat = [[0.0 for _ in range(self.n)] for _ in range(self.n)]
        self.determinant = None
    
    def printMat(self):
        for i in range(self.n):
            for j in range(self.n):
                print(f"{self.mat[i][j]} ", end="\t")
            print("\b")

    def setRow(self, row_num, row_data):
        for c in range(self.n):
            self.mat[row_num][c] = row_data[c]

    def getCopyMat(self):
        c = SquareMatrix()
        c.setSize(self.n)

        c.mat = [[self.mat[r][c] for c in range(self.n)] for r in range(self.n)]
        
        return c

    def mulScalar(self, scalar):
        for r in range(self.n):
            for c in range(self.n):
                self.mat[r][c] *= scalar
    
    def divScalar(self, scalar):
        if scalar == 0:
            return
        
        for r in range(self.n):
            for c in range(self.n):
                self.mat[r][c] /= scalar

    def compareMat(self, other):
        if self.n != other.n:
            return False
        
        for r in range(self.n):
            for c in range(self.n):
                if self.mat[r][c] != other.mat[r][c]:
                    return False
        
        return True

    def matMul(self, other):
        result = SquareMatrix()
        result.setSize(self.n)

        for i in range(self.n):
            for j in range(self.n):
                temp = 0
                for k in range(self.n):
                    temp += self.mat[i][k] * other.mat[k][j]
                result.mat[i][j] = temp
        
        return result

    # FOR INVERSE BY DETERMINANT
    def getTransposeMat(self):
        trans = SquareMatrix()
        trans.setSize(self.n)
        trans.mat = [[self.mat[j][i] for j in range(self.n)] for i in range(self.n)]
        return trans
    
    def getMinorMat(self, i, j):
        minor = SquareMatrix()
        minor.setSize(self.n - 1)
        minor.mat = [row[:j] + row[j+1:] for row in (self.mat[:i] + self.mat[i+1:])]
        return minor
    
    def calMatDeterminant(self):
        if self.determinant != None:
            return self.determinant

        if self.n == 1:
            self.determinant = self.mat[0][0]
        elif self.n == 2:
            self.determinant = self.mat[0][0] * self.mat[1][1] - self.mat[0][1] * self.mat[1][0]
        else:
            self.determinant = 0
            for c in range(self.n):
                self.determinant += ((-1) ** c) * self.mat[0][c] * self.getMinorMat(0, c).calMatDeterminant()
        
        return self.determinant
        
    def hasInverseByDeterminant(self):
        if self.determinant == None:
            self.calMatDeterminant()
        
        if abs(self.determinant) < 1e-10:
            print("행렬식이 0이므로 역행렬이 없습니다")
            return False
        return True

    def getInverseByDeterminant(self):
        if not self.hasInverseByDeterminant():
            return None
        print(f"행렬식 : {self.determinant} (테스트를 위해 잠시 추가됨.)")
        
        inverseMat = SquareMatrix()
        inverseMat.setSize(self.n)

        if self.n == 1:
            inverseMat[0][0] = 1.0 / self.mat[0][0]
        elif self.n == 2:
            inverseMat.mat = [[self.mat[1][1], (-1) * self.mat[0][1]],
                              [(-1) * self.mat[1][0], self.mat[0][0]]]
            inverseMat.divScalar(self.determinant)
        else:
            cofactorMat = SquareMatrix()
            cofactorMat.setSize(self.n)
            for row in range(self.n):
                cofactorRow = []
                for col in range(self.n):
                    minor = self.getMinorMat(row, col)
                    cofactorRow.append(((-1) ** (row+col)) * minor.calMatDeterminant())
                cofactorMat.setRow(row, cofactorRow)

            inverseMat = cofactorMat.getTransposeMat()
            inverseMat.divScalar(self.determinant)

            return inverseMat

    # FOR INVERSE BY GAUSSJORDAN
    def getInverseByGaussJordan(self):
        matCopy = self.getCopyMat()

        unitMat = SquareMatrix()
        unitMat.setSize(self.n)
        for i in range(self.n):
            unitMat.mat[i][i] = 1.0

        for c in range(self.n):
            # 각각의 첫번째 행의 c번째 값이 0이 아닌 행의 c번째 값을 1로 만들기
            for r in range(self.n - c):
                if matCopy.mat[r][c] != 0:
                    divNum = matCopy.mat[r][c]
                    matCopy.mat.append([x/divNum for x in matCopy.mat[r]])
                    del matCopy.mat[r]

                    unitMat.mat.append([x/divNum for x in unitMat.mat[r]])
                    del unitMat.mat[r]
                    break
            
            # 각 행에 맞게 소거해주기
            for r in range(self.n - 1):
                mulNum = matCopy.mat[r][c]

                temp = [l * mulNum for l in matCopy.mat[-1]] # 가우스 조던 소거를 위해 각행에 빼줄 값
                matCopy.mat[r] = [matCopy.mat[r][k] - temp[k] for k in range(self.n)]

                temp = [l * mulNum for l in unitMat.mat[-1]]
                unitMat.mat[r] = [unitMat.mat[r][k] - temp[k] for k in range(self.n)]
        
        # 대각선의 곱이 0인 경우에는 역행렬 없음
        hasInverse = 1
        for i in range(self.n):
            hasInverse *= unitMat.mat[i][i]
        
        if hasInverse == 0:
            print("역행렬이 없습니다.")
            return None
        
        return unitMat

###############################################################################################################################

def main():
    try:
        matrix_a = SquareMatrix()

        k = int(input("정방행렬의 차수를 입력하시오. : "))
        if (k <= 0):
            print("차수는 양의 정수여야 합니다")
            return
        matrix_a.setSize(k)

        print(f"{k}*{k}  정방행렬 A를 입력하시오. (각 행을 공백으로 구분하여 한 줄 식 입력): ")
        for i in range(k):
            while True:
                try:
                    row_input = input(f"{i+1}행 : ").strip()
                    row_values = [float(x) for x in row_input.split()]
                    if len(row_values) != k:
                        print(f"입력 오류: 정확히 {k}개의 값을 입력하시오.")
                        continue
                    matrix_a.setRow(i, row_values)
                    break
                except ValueError:
                    print("입력 오류: 숫자만 입력")

        print()
        inverseMatAByDeterminant = matrix_a.getInverseByDeterminant()
        if inverseMatAByDeterminant != None:
            print("행렬식을 이용한 역행렬: ")
            inverseMatAByDeterminant.printMat()

        print()
        inverseMatAByGaussJordan = matrix_a.getInverseByGaussJordan()
        if inverseMatAByGaussJordan != None:
            print("가우스 조던 소거법을 이용한 역행렬: ")
            inverseMatAByGaussJordan.printMat()
        
        if inverseMatAByDeterminant != None and inverseMatAByGaussJordan != None:
            if inverseMatAByDeterminant.compareMat(inverseMatAByGaussJordan):
                print("역행렬 계산 결과가 동일함")
                unitMat = SquareMatrix()
                unitMat.setSize(inverseMatAByDeterminant.n)
                for i in range(inverseMatAByDeterminant.n):
                    unitMat.mat[i][i] = 1.0

                if unitMat.compareMat(inverseMatAByDeterminant.matMul(matrix_a)):
                    print("역산 결과도 동일함.")
                else:
                    print("역산 결과가 다름")
            else:
                print("역행렬 계산 결과가 다름")

    except ValueError:
        print("입력 오류: 정수를 입력하시오.")
    except Exception as e:
        print(f"예기치 못한 오류: {e}")


if __name__ == "__main__":
    main()