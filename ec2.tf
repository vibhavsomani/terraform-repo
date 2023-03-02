resource "aws_instance" "foo" {
  ami           = "ami-0c435d654482161c5"
  instance_type = "t2.micro"
}
